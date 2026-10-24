"""Пакет утилиты CalcFilesControlSum - подсчёт и проверка контрольных сумм файлов.

Публичный API:
- Config / ConfigReader / ConfigWriter - работа с конфигурацией (секции ключ-значение);
- cfcs - CLI-точка входа (запуск: python -m calc_files_control_sum.cfcs);
- my_utils, my_strings, str_without_trans - вспомогательные модули.
"""

from . import my_strings
from . import str_without_trans
from . import config
from . import my_utils
from .config import Config, ConfigReader, ConfigWriter

# Номер версии должен совпадать с номером версии в setup.cfg
__version__ = "1.2.1"

__all__ = [
    "Config",
    "ConfigReader",
    "ConfigWriter",
    "__version__",
    "config",
    "my_strings",
    "my_utils",
    "str_without_trans",
]
