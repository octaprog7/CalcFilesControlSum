"""Класс, позволяющий сохранять и считывать из файла группы параметров
типа ключ-значение, сгруппированные в именованные разделы или секции.
Ключом может быть только строка. Значением может быть строка или число."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import IO
import io

import my_strings


class Config(ABC):
    """base class for work with simple key-value config separated by sections"""
    SEC_NAME_START = "{"
    SEC_NAME_END = "}"
    min_section_name_length = 5

    def __init__(self, filename_or_fileobject: [str, IO]):
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
            raise ValueError(f"Invalid input parameter: {filename_or_fileobject}")

    @abstractmethod
    def _open(self, filename: str):
        pass

    @staticmethod
    def get_section_header(section_name: str):
        return f"{Config.SEC_NAME_START}{section_name}{Config.SEC_NAME_END}"

    def __del__(self):
        if self._f_name and self._fp:
            self._fp.close()
            del self._fp


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
    def _open(self, filename: str) -> IO:
        return open(file=filename, mode="w", encoding="utf-8")

    @staticmethod
    def _get_line(key: str, value: str) -> str:
        """for class internal use"""
        return f"{str(key)}{my_strings.strCS_filename_splitter}{str(value)}"

    def write_section(self, name: str, keys_and_values: Iterable[tuple[str, str]] or None):
        """write section with name to file
        if keys_and_values is None, write section header only"""
        line = self.get_section_header(name)
        self.write_line(line)
        if keys_and_values is None:
            return
        for k, v in keys_and_values:
            self.write_line(self._get_line(k, v))

        # empty string
        self.write_line("")

    def write_line(self, line: str):
        """write only one line(s) to file or stream"""
        print(line, file=self._fp)


class ConfigReader(Config):
    """Read configuration from file"""
    def _open(self, filename: str) -> IO:
        return open(file=filename, encoding="utf-8")

    def read(self, section_name: str = "") -> Iterable[tuple[str, str]]:
        """Iterable reading config file. function-generator.
        if section_name is empty (""), this method read all section with their names,
        In this case, at the beginning of the section, the method returns only one value - its name!

        if section_name not empty, this method read only one section
        In this case, the method returns only the key-value pairs of the specified section!
        """
        current_section_name = None
        for line in self._fp:
            parts = line.strip().split(sep=my_strings.strCS_filename_splitter)
            key, value = parts[0].strip(), None
            if not key:
                continue  # empty string
            if len(parts) > 1:
                value = parts[1].strip()
            if value is None:  # key only:
                if key.startswith(Config.SEC_NAME_START) and key.endswith(Config.SEC_NAME_END):
                    if len(key) < Config.min_section_name_length:
                        raise ValueError(f"Invalid section name length!: {key}")
                    current_section_name = key[1:-1]
                    if not section_name:
                        yield current_section_name  # return section name only!
                    continue

            if section_name and current_section_name == section_name:
                yield key, value  # filtered output. return key, value pair
            if not section_name:
                yield key, value  # return key, value pair. Not filtered output. Return All!

        # return current file position
        return self._fp.tell()
