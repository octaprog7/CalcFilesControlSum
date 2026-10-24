"""Класс, позволяющий сохранять и считывать из файла группы параметров
типа ключ-значение, сгруппированные в именованные разделы или секции.
Ключом может быть только строка. Значением может быть строка или число."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import IO, overload
import io
import hashlib
import calc_files_control_sum.my_strings as my_strings
import calc_files_control_sum.str_without_trans as swtrans


class Config(ABC):
    """base class for work with simple key-value config separated by sections"""
    SEC_NAME_START = "{"
    SEC_NAME_END = "}"
    min_section_name_length = 5
    default_encoding = "utf-8"

    def __init__(self, filename_or_fileobject: str | IO, check_crc: bool = False,
                 def_encoding=default_encoding):
        # подсчитать crc перед записью настроек или нет!
        self._check_crc = check_crc
        # кодировка файлов по умолчанию!
        self._default_enc = def_encoding  # = locale.getpreferredencoding()
        if isinstance(filename_or_fileobject, str):
            self._f_name = filename_or_fileobject
            self._fp = None
            # открываю классический файл на диске
            self._fp = self._open(self._f_name)
        elif isinstance(filename_or_fileobject, io.TextIOWrapper):
            # операции будут производится над уже созданным файловым объектом (например sys.stdout)
            self._fp = filename_or_fileobject
            self._f_name = None
        else:
            raise ValueError(f"{my_strings.strInvalidInputParameter}: {filename_or_fileobject}")
        if self._check_crc:
            self.hash = hashlib.new(swtrans.default_cfg_crc_alg)

    @property
    def check_crc(self) -> bool:
        return self._check_crc

    @property
    def default_enc(self) -> str:
        return self._default_enc

    @check_crc.setter
    def check_crc(self, value: bool):
        self._check_crc = value

    @abstractmethod
    def _open(self, filename: str):
        pass

    @staticmethod
    def get_section_header(section_name: str):
        return f"{Config.SEC_NAME_START}{section_name}{Config.SEC_NAME_END}"

    def _close_file(self):
        """Закрывает файл, открытый конструктором по имени.
        Внешние файловые объекты (sys.stdout) не закрываются!"""
        f_name = getattr(self, "_f_name", None)
        fp = getattr(self, "_fp", None)
        if f_name and fp:
            try:
                fp.close()
            except Exception:
                pass
            self._fp = None

    def close(self):
        """Закрывает файл. Для ConfigWriter дополнительно дописывает CRC-строку в конец отчёта."""
        self._close_file()

    def __enter__(self):
        """Поддержка конструкции 'with': возвращает сам объект."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Гарантирует вызов close() при выходе из 'with'.
        Возвращает False - исключения не подавляются!"""
        self.close()
        return False

    def __del__(self):
        # защитный откат: закрывает файл (для Writer - ещё и дописывает CRC).
        # Момент вызова непредсказуем, поэтому в main() используется явный close()!
        try:
            self.close()
        except Exception:
            # в __del__ исключения недопустимы (в т.ч. для частично
            # проинициализированного объекта после падения конструктора)
            pass


class ConfigWriter(Config):
    """Make config file.
    Example:
    a = range(10)
    b = range(20, 30)
    z = zip(a, b)

    from Config import ConfigWriter
    cw = ConfigWriter("myconfig.cfg")
    cw.write_section("section_name", z)
    """

    def __init__(self, filename_or_fileobject: str | IO, check_crc: bool = False,
                 def_encoding=Config.default_encoding):
        super().__init__(filename_or_fileobject, check_crc, def_encoding)
        # признак того, что CRC-строка уже была дописана в конец отчёта
        self._crc_written = False

    def _open(self, filename: str) -> IO:
        return open(file=filename, mode="w", encoding=self.default_enc)

    @staticmethod
    def _get_line(key: str, value: str) -> str:
        """for class internal use"""
        return f"{str(key)}{swtrans.strCS_filename_splitter}{str(value)}"

    def write_section(self, name: str, keys_and_values: Iterable[tuple[str, str]] | None):
        """write section with name to file
        if keys_and_values is None, write section header only"""
        line = self.get_section_header(name)
        # запись заголовка
        self.write_line(line)
        if keys_and_values is None:
            return
        # запись содержимого
        for k, v in keys_and_values:
            line = self._get_line(k, v)
            self.write_line(line)

        # empty string
        self.write_line("")

    def write_line(self, line: str):
        """write only one line(s) to file or stream"""
        if self.check_crc:
            self.hash.update(bytes(line, encoding=self.default_enc))
        print(line, file=self._fp)

    def close(self):
        """Завершает запись: дописывает CRC-строку и закрывает файл."""
        if getattr(self, "check_crc", False) and not getattr(self, "_crc_written", False):
            line = self._get_line(swtrans.strCRClabel, self.hash.hexdigest().upper())
            self.write_line(line)
            self._crc_written = True
        self._close_file()
        # __del__ не переопределяется: базовый Config.__del__ через self.close()
        # вызывает этот метод и допишет CRC в файл контрольных сумм!


class ConfigReader(Config):
    """Read configuration from file"""
    def _open(self, filename: str) -> IO:
        # Открываю файл один раз: проверка CRC и чтение данных выполняются одним дескриптором ФС.
        cfg_file = open(file=filename, mode="r", encoding=self.default_enc)
        try:
            if self.check_crc:
                # Проход 1: поиск CRC-строки (hash_val). Имя алгоритма подписи в файле
                # с КС не хранится, поэтому алгоритм определяется по длине хэш-строки:
                # 32 символа - md5 (файлы, созданные старыми версиями утилиты),
                # 64 символа - sha256 (новая версия). Для сохранения обратной совместимости!
                crc_read = False
                crc = ""
                for line in cfg_file:
                    if line.startswith(swtrans.strCRClabel):
                        crc_parts = line.strip().split(sep=swtrans.strCS_filename_splitter)
                        if len(crc_parts) < 2 or not crc_parts[1].strip():
                            # строка CRC присутствует, но её значение отсутствует - файл битый!
                            raise ValueError(f"{filename}. {my_strings.strInvalidCrcValue}")
                        crc = crc_parts[1].strip()
                        crc_read = True
                        break
                if crc_read:
                    crc_alg = "sha256" if len(crc) == 64 else ("md5" if len(crc) == 32 else None)
                    if crc_alg is None:
                        raise ValueError(f"{filename}. {my_strings.strInvalidCrcValue}")
                    # Проход 2: вычисляю хэш содержимого файла (без CRC-строки) от начала
                    lhash = hashlib.new(crc_alg)
                    cfg_file.seek(0)
                    for line in cfg_file:
                        if line.startswith(swtrans.strCRClabel):
                            break
                        # удаляю символы перевода строки (\n) и возврата каретки (\r),
                        # т. к. их нет в хэшируемых данных: print() на Windows добавляет \r\n
                        lhash.update(bytes(line.rstrip("\r\n"), encoding=self.default_enc))
                    calcul = lhash.hexdigest().upper()
                    # print(f"The hashes matched! From file: {crc}\tCalculated: {calculated}")
                    if crc != calcul:
                        raise ValueError(f"{filename}. {my_strings.strInvalidCrcValue}: {crc}, "
                                         f"{my_strings.strCalcul}: {calcul}.")
                else:
                    # Строка CRC (hash_val) в файле не найдена. Это не ошибка:
                    # допускается работа с файлами контрольных сумм (КС), созданными старыми
                    # версиями утилиты (до введения CRC-защиты), в которых CRC-строки ещё не было.
                    # Проверка целостности пропускается - это осознанная обратная совместимость.
                    # Предупреждение не выводится в stdout, так-как stdout используется
                    # для формирования файла отчёта, и посторонние сообщения испортят его формат.
                    pass
                # Перематываю файл в начало для последующего чтения данных.
                cfg_file.seek(0)
        except ValueError:
            # при повреждении CRC  закрываю файл и выбрасываю ошибку
            cfg_file.close()
            raise
        return cfg_file

    @overload
    def read(self, section_name: str) -> Iterable[tuple[str, str]]:
        """Read only one section: returns key-value pairs only."""

    @overload
    def read(self, section_name: str = "") -> Iterable[tuple[str, str | None] | str]:
        """Read all sections: returns section names (str) and key-value pairs (tuple)."""

    def read(self, section_name: str = "") -> Iterable[tuple[str, str | None] | str]:
        """Iterable reading config file. function-generator.
        if section_name is empty (""), this method read all section with their names,
        In this case, at the beginning of the section, the method returns only one value - its name!

        if section_name not empty, this method read only one section
        In this case, the method returns only the key-value pairs of the specified section!
        """
        current_section_name = None
        for line in self._fp:
            # Убираю переводы строк (\n, \r), но не пробелы: имена файлов
            # могут содержать ведущие/концевые пробелы, которые нельзя терять!
            line = line.rstrip("\r\n")
            parts = line.split(sep=swtrans.strCS_filename_splitter)
            key, value = parts[0].strip(), None
            if not key:
                continue  # empty string
            if len(parts) > 1:
                # Значение не обрезаю (strip): имя файла может иметь пробелы по краям!
                value = parts[1]
            if value is None:  # key only:
                if key.startswith(Config.SEC_NAME_START) and key.endswith(Config.SEC_NAME_END):
                    if len(key) < Config.min_section_name_length:
                        raise ValueError(f"{my_strings.strInvalidSectionNameLength}: {key}")
                    current_section_name = key[1:-1]
                    if not section_name:
                        yield current_section_name  # return section name only!
                    continue

            if section_name and current_section_name == section_name:
                yield key, value  # filtered output. return key, value pair
            if not section_name:
                yield key, value  # return key, value pair. Not filtered output. Return All!
