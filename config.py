"""Класс, позволяющий сохранять и считывать из файла группы параметров
типа ключ-значение, сгруппированные в именованные разделы или секции.
Ключом может быть только строка. Значением может быть строка или число."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import IO


class Config(ABC):
    """base class for work with simple key-value config separated by sections"""
    SEC_NAME_START = "{"
    SEC_NAME_END = "}"
    KEY_VAL_DELIM = "\t"

    def __init__(self, filename: str):
        self._f_name = filename
        self._fp = None
        self._fp = self._open(self._f_name)

    @abstractmethod
    def _open(self, filename: str):
        pass

    @staticmethod
    def get_section_header(section_name: str):
        return f"{Config.SEC_NAME_START}{section_name}{Config.SEC_NAME_END}"

    def __del__(self):
        if self._fp:
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

    def _get_line(self, key: str, value: str) -> str:
        """for class internal use"""
        return f"{str(key)}{self.KEY_VAL_DELIM}{str(value)}"

    def write_section(self, name: str, keys_and_values: Iterable[tuple[str, str]]):
        """write section with name to file"""
        line = self.get_section_header(name)
        print(line, file=self._fp)
        for k, v in keys_and_values:
            print(self._get_line(k, v), file=self._fp)

        # empty string
        print("", file=self._fp)


class ConfigReader(Config):
    """Read configuration from file"""
    def _open(self, filename: str) -> IO:
        return open(file=filename, encoding="utf-8")

    def read(self, section_name: str = "") -> Iterable[tuple[str, str, str]]:
        """Iterable reading config file. function-generator.
        if section_name is empty (""), this method read all section with their names,
        In this case, at the beginning of the section, the method returns only one value - its name!

        if section_name not empty, this method read only one section
        In this case, the method returns only the key-value pairs of the specified section!
        """
        current_section_name = None
        for line in self._fp:
            parts = line.strip().split(sep=Config.KEY_VAL_DELIM)
            key, value = parts[0].strip(), None
            if not key:
                continue  # empty string
            if len(parts) > 1:
                value = parts[1].strip()
            if value is None:  # and section_name:
                if key.startswith(Config.SEC_NAME_START) and key.endswith(Config.SEC_NAME_END):
                    current_section_name = key[1:-1]
                    if not section_name:
                        yield current_section_name  # return section name only!
                    continue

            if section_name and current_section_name == section_name:
                yield key, value  # filtered output. return key, value pair
            if not section_name:
                yield key, value  # return key, value pair

        # return current file position
        return self._fp.tell()
