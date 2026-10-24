#!/usr/bin/env python3
"""service utils"""
import os
import hashlib
import pathlib
import datetime
import calc_files_control_sum.my_strings as my_strings
import calc_files_control_sum.str_without_trans as swtrans
import calc_files_control_sum.config as config


def _to_path(full_path: str) -> pathlib.Path:
    """Метод создания pathlib.Path из строки пути."""
    return pathlib.Path(full_path)


def get_hash_file(full_path_to_file: str, algorithm="md5", buff_size=16384) -> str:
    """return hash of file. Выбрал размер буфера чтения по результатам бенчмарка:
    зависимость скорости чтения от размера буфера (файл 512 МиБ, sha256):
    4К -> 800 MiB/s; 16К -> 1208 MiB/s; 64К -> 1398; 1М -> 1479; 4М-16М - хуже.
    16 Кбайт - баланс скорости и расхода памяти на буфер!"""
    h = hashlib.new(algorithm)
    with open(full_path_to_file, "rb") as f:
        for chunk in iter(lambda: f.read(buff_size), b""):
            h.update(chunk)

    return h.hexdigest().upper()


def calc_mib_per_sec(total_bytes: int, delta_sec: float) -> float:
    """Скорость обработки данных в MiB/с.
    При delta_sec <= 0 возвращает 0.0 (защита от деления на ноль)!"""
    MIB_1 = 1024 * 1024
    return (total_bytes / MIB_1 / delta_sec) if delta_sec > 0 else 0.0


def escape_file_name(file_name: str) -> str:
    """Экранирует обратный слеш и табуляцию в имени файла для записи в отчёт.
    Табуляция - разделитель полей строки отчёта, поэтому экранируется,
    чтобы имя файла с табуляцией не ломало формат файла контрольных сумм!"""
    return file_name.replace("\\", "\\\\").replace("\t", "\\t")


def unescape_file_name(file_name: str) -> str:
    """Восстанавливает имя файла из строки отчёта (обратное экранирование:
    \\t -> табуляция, \\\\ -> обратный слэш). Неизвестные escape-
    последовательности сохраняются как есть."""
    res = []
    i = 0
    while i < len(file_name):
        if file_name[i] == "\\" and i + 1 < len(file_name):
            nxt = file_name[i + 1]
            if nxt == "t":
                res.append("\t")
            elif nxt == "\\":
                res.append("\\")
            else:
                # неизвестная escape-последовательность - сохраняю оба символа
                res.append(file_name[i])
                res.append(nxt)
            i += 2
            continue
        res.append(file_name[i])
        i += 1
    return "".join(res)


def is_folder_exist(full_folder_path: str) -> bool:
    """check folder for exist and is folder return value is Boolean!"""
    return _to_path(full_folder_path).is_dir()


def is_file_exist(filename: str) -> bool:
    """check file for exist"""
    return _to_path(filename).is_file()


def get_owner_folder_path(full_path_to_file: str) -> str:
    """ return owner folder path from full path file name """
    return str(_to_path(full_path_to_file).parent)


def get_file_name_from_path(full_path_to_file: str) -> str:
    """ return filename from full path file name """
    return _to_path(full_path_to_file).name


def get_file_extension_from_path(full_path_to_file: str) -> str:
    """ return file extension from full path file name """
    return _to_path(full_path_to_file).suffix


def split_path(full_path_to_file: str) -> tuple[str, str, str]:
    """Divides the file path into three parts: parent (owner folder name),
    name (file name), suffix(ext)"""
    path = _to_path(full_path_to_file)
    return str(path.parent), path.name, path.suffix


class DeltaTime:
    """time interval measurement"""
    @staticmethod
    def get_time() -> datetime.datetime:
        """return time in second"""
        return datetime.datetime.now()

    def _reset(self):
        """Сброс измерения. Задаю новый стартовый момент начала интервала."""
        self._start = DeltaTime.get_time()
        self._stop = None

    def __init__(self):
        self._reset()

    def start(self):
        """call start before measurement"""
        # сброс в _reset()!
        self._reset()

    def delta(self) -> float:
        """return delta time in second"""
        self._stop = DeltaTime.get_time()
        return self._stop.timestamp() - self._start.timestamp()

    def __float__(self) -> float:
        """float(dt) - интервал измерения в секундах (эквивалент delta())"""
        return self.delta()

    def __str__(self) -> str:
        """str(dt) - наглядное представление интервала измерения"""
        return (f"DeltaTime(start={self._start}, stop={self._stop}, "
                f"delta={self.delta():.3f}s)")

    @property
    def start_time(self) -> datetime.datetime:
        return self._start

    @property
    def stop_time(self) -> datetime.datetime:
        """Время остановки измерения. Верно только после вызова delta(), до вызова возвращает None!"""
        return self._stop


def settings_from_file(filename: str, check_crc: bool = True) -> dict:
    """Read all settings from file and convert it into dict"""
    try:
        cr = config.ConfigReader(filename, check_crc=check_crc)
        res = dict(cr.read(swtrans.str_settings_header))
    except OSError as e:
        print(f"{my_strings.strOsError}: {e}")
        return {}
    if "ext" in res and isinstance(res["ext"], str):
        # преобразование строки в список с расширениями!
        lst = res["ext"].replace("[", "").replace("]", "").split(sep=",")
        res["ext"] = lst
    return res


def get_file_stat(filename: str) -> os.stat_result:
    """Return statistic of file. Pls. see: https://docs.python.org/3.9/library/os.html#os.stat_result"""
    path = pathlib.Path(filename)
    return path.stat()
