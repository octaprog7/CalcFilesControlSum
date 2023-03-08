"""реализация интернационализации.
Если что, я знаю про gettext"""
from abc import ABC, abstractmethod
import csv
import sqlite3


class IDataProvider(ABC):
    """Поставщик данных (ключ-значение)"""
    @abstractmethod
    def get_value(self, key: str) -> str:
        ...

    def __call__(self, key: str):
        return self.get_value(key)

    @abstractmethod
    def __len__(self):
        ...


class CSVProvider(IDataProvider):
    """CSV internationalization data provider"""
    def __init__(self, file_name: str, key_field_name: str, lang: str, default_lang="EN"):
        self._storage = file_name
        self._key_field = key_field_name
        self._value_field = lang
        self._vals = dict()
        # заполнение словаря
        try:
            self._fill_stor(self._key_field, lang)
        except IndexError:
            pass
        except LookupError:
            pass
        except ValueError:
            pass
        else:
            return  # исключения не было!
        # было исключение, возможно задан неверный язык локализации
        # последняя попытка с языком по умолчанию
        self._fill_stor(self._key_field, default_lang)

    def _fill_stor(self, key: str, value: str):
        self._vals.clear()
        for k, v in self._get_fields_by_names((key, value)):
            self._vals[k] = v

    def _get_fields_by_names(self, column_names: [tuple, list], delimiter: str = ',') -> tuple:
        """Итератор, который возвращает за каждый вызов кортеж из полей csv файла, имена которых (первая строка),
        в виде строк, содержит последовательность field_names"""
        with open(self._storage, mode='r', encoding="utf-8", newline='') as csv_file:
            row_reader = csv.reader(csv_file, delimiter=delimiter)
            _b = True
            for _row in row_reader:
                if _b:  # первая строка cvs файла должна содержать названия столбцов! создание кортежа индексов столбцов
                    column_indexes = [_row.index(column_name) for column_name in column_names]
                    _b = False
                # кортеж значений строк нужных столбцов
                yield tuple([_row[_index] for _index in column_indexes])

    def get_value(self, key: str) -> str:
        return self._vals[key]

    def __len__(self):
        return len(self._vals)


class SQLiteDataProvider(IDataProvider):
    """SQLite internationalization data provider"""

    def __init__(self, connection_string: str, key_field_name: str, lang: str, default_lang="EN"):
        self._conn_str = connection_string
        self._key_field = key_field_name
        self._value_field = lang
        self._vals = dict()
        # заполнение словаря
        try:
            self._fill_stor(self._key_field, lang)
        except sqlite3.Error:
            pass
        except ValueError:
            pass
        else:
            return  # исключения не было!
        # было исключение, возможно задан неверный язык локализации
        # последняя попытка с языком по умолчанию
        self._fill_stor(self._key_field, default_lang)

    def _fill_stor(self, key: str, value: str):
        self._vals.clear()
        for k, v in self._get_fields_by_names(key, value):
            self._vals[k] = v

    def _get_fields_by_names(self, str_id_column_name: str, lang_column_name: str) -> tuple:
        """Итератор, который возвращает за каждый вызов кортеж из полей csv файла, имена которых (первая строка),
        в виде строк, содержит последовательность field_names"""
        with sqlite3.connect(f"file:{self._conn_str}?mode=ro") as connection:     # open as read only!
            str_sql = f"select {str_id_column_name}, {lang_column_name} from istrings;"
            for row in connection.execute(str_sql):
                yield row   # кортеж значений строк нужных столбцов

    def get_value(self, key: str) -> str:
        return self._vals[key]

    def __len__(self):
        return len(self._vals)
