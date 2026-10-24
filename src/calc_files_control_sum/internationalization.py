"""реализация интернационализации.
Если что, я знаю про gettext"""
import csv
import logging
import sqlite3
from abc import ABC, abstractmethod
from collections.abc import Iterator

_log = logging.getLogger(__name__)


class LocalizationError(LookupError):
    """Ошибка загрузки переводов: отсутствующий файл, пустой файл,
    не найденная колонка/язык, битые данные и т.п."""


class IDataProvider(ABC):
    """Поставщик данных (ключ-значение)"""
    def __init__(self, key_field_name: str, lang: str, default_lang: str) -> None:
        self._key_field = key_field_name
        self._value_field = lang
        self._default_lang = default_lang
        self._vals: dict[str, str] = {}
        self._lang: str = lang
        self._load()

    @abstractmethod
    def _iter_fields(self, key_column: str, value_column: str) -> Iterator[tuple[str, str]]:
        """Итератор пар (ключ, значение) из источника данных для указанных колонок.

        При ошибках чтения или некорректных данных бросает LocalizationError
        с описанием причины.
        """
        ...

    def _load(self) -> None:
        """Заполнение словаря переводов.

        Сначала пробует запрошенный язык; при неудаче делается попытка
        с языком по умолчанию. Если обе попытки неудачны -> бросает
        LocalizationError с полным описанием ошибки.
        """
        errors: list[str] = []
        for lang in (self._value_field, self._default_lang):
            try:
                self._vals = dict(self._iter_fields(self._key_field, lang))
            except Exception as exc:  # noqa: BLE001 - нужен полный контекст ошибки
                errors.append(f"language '{lang}': {type(exc).__name__}: {exc}")
                _log.warning("Failed to load translations for the language '%s': %s", lang, exc)
            else:
                self._lang = lang
                _log.info("Translations loaded: %d (language '%s')", len(self._vals), lang)
                return
        raise LocalizationError(
            "Failed to load translations: requested language '%s' and default language '%s' "
            "are unavailable. Reasons: %s" % (self._value_field, self._default_lang, "; ".join(errors))
        )

    def get_value(self, key: str) -> str:
        try:
            return self._vals[key]
        except KeyError:
            raise KeyError(f"No translation for the key '{key}' (language '{self._lang}')") from None

    def get(self, key: str, default=None):
        """Возвращает перевод для ключа или default, если ключ отсутствует."""
        return self._vals.get(key, default)

    def __call__(self, key: str):
        return self.get_value(key)

    def __contains__(self, key: object) -> bool:
        return key in self._vals

    def __len__(self) -> int:
        return len(self._vals)


class CSVProvider(IDataProvider):
    """CSV internationalization data provider"""
    def __init__(self, file_name: str, key_field_name: str, lang: str, default_lang: str = "EN"):
        self._storage = file_name
        super().__init__(key_field_name, lang, default_lang)

    def _iter_fields(self, key_column: str, value_column: str) -> Iterator[tuple[str, str]]:
        """Итератор пар (ключ, значение) из CSV-файла.

        Первая строка файла считается заголовком и должна содержать имена колонок.
        Файл читается как utf-8 (в т.ч. с BOM).
        """
        try:
            csv_file = open(self._storage, mode="r", encoding="utf-8-sig", newline="")
        except OSError as exc:
            raise LocalizationError(f"Failed to open CSV file '{self._storage}': {exc}") from exc
        with csv_file:
            row_reader = csv.reader(csv_file)  # разделитель по умолчанию ','
            try:
                header = next(row_reader)
            except StopIteration:
                raise LocalizationError(f"CSV file '{self._storage}' is empty (no header row)") from None
            try:
                column_indexes = [header.index(column_name) for column_name in (key_column, value_column)]
            except ValueError:
                raise LocalizationError(
                    f"CSV file '{self._storage}' does not contain columns "
                    f"'{key_column}' and/or '{value_column}'; available: {header}"
                ) from None
            for line_no, row in enumerate(row_reader, start=2):
                if not row:  # пустая строка в конце файла
                    continue
                try:
                    yield row[column_indexes[0]], row[column_indexes[1]]
                except IndexError:
                    raise LocalizationError(
                        f"CSV file '{self._storage}', line {line_no}: the row has fewer fields "
                        f"than expected (need at least {max(column_indexes) + 1})"
                    ) from None

    def get_value(self, key: str) -> str:
        return super().get_value(key)

    def __len__(self) -> int:
        return len(self._vals)


class SQLiteDataProvider(IDataProvider):
    """SQLite internationalization data provider"""

    def __init__(self, connection_string: str, key_field_name: str, lang: str, default_lang: str = "EN"):
        self._conn_str = connection_string
        super().__init__(key_field_name, lang, default_lang)

    @staticmethod
    def _table_columns(connection: sqlite3.Connection) -> set[str]:
        """Имена колонок таблицы 'istrings'."""
        return {row[1] for row in connection.execute("PRAGMA table_info(istrings)")}

    def _iter_fields(self, key_column: str, value_column: str) -> Iterator[tuple[str, str]]:
        """Итератор пар (ключ, значение) из таблицы 'istrings' базы SQLite.

        База открывается только на чтение. Имена колонок сначала проверяются
        через PRAGMA table_info, поэтому не могут быть источником SQL-инъекции.
        """
        try:
            connection = sqlite3.connect(f"file:{self._conn_str}?mode=ro", uri=True)
        except sqlite3.Error as exc:
            raise LocalizationError(f"Failed to open SQLite database '{self._conn_str}': {exc}") from exc
        try:
            existing = self._table_columns(connection)
            missing = [name for name in (key_column, value_column) if name not in existing]
            if missing:
                raise LocalizationError(
                    f"The table 'istrings' in database '{self._conn_str}' has no columns {missing}; "
                    f"available: {sorted(existing)}"
                )
            str_sql = f'SELECT "{key_column}", "{value_column}" FROM istrings'
            for row in connection.execute(str_sql):
                yield row[0], row[1]
        finally:
            connection.close()

    def get_value(self, key: str) -> str:
        return super().get_value(key)

    def __len__(self) -> int:
        return len(self._vals)
