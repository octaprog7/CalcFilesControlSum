#!/usr/bin/env python3
"""Utility to calc files control sum in specified folder.
    Type --help for command line parameters description."""

import argparse
import pathlib
import sys
import fnmatch
import os
import hashlib
from collections.abc import Iterable

import calc_files_control_sum.my_utils as my_utils
import calc_files_control_sum.my_strings as my_strings
import calc_files_control_sum.str_without_trans as swtrans
import calc_files_control_sum.config as config
from calc_files_control_sum import __version__


def process(full_path_to_folder: str, patterns: list, alg: str) -> Iterable[tuple[str, str, int]]:
    """Перечисляет файлы внутри папки, подсчитывая их контрольную сумму,
    получая имя файла и его размер в байтах.
    Функция-генератор.
    ВНИМАНИЕ: обход папки не рекурсивный - обрабатываются только
    файлы верхнего уровня, файлы во вложенных папках игнорируются!"""
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            for pattern in patterns:
                if fnmatch.fnmatch(child.name, pattern):
                    try:
                        # Получаю размер файла до вычисления хэша. Он должен
                        # соответствовать читаемому содержимому
                        file_size = child.stat().st_size
                        # file checksum calculation
                        loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                    except OSError as e:
                        # Пропускаю недоступный или удалённый во время сканирования файл,
                        # не прерывая создание всего отчёта!
                        # Вывожу сообщение в stderr, чтобы не испортить отчёт в stdout.
                        print(f"{my_strings.strOsError}: {e}", file=sys.stderr)
                        break
                    yield loc_hash, child.name, file_size
                    break


# parse_files_info
def parse_control_sum_file(control_sum_filename: str, settings: dict) -> Iterable[tuple[str, str]]:
    """разбор файла на имена файлов и их контрольные суммы!
    Функция-генератор"""
    fld = settings["src"]
    # вычислять CRC не нужно!
    cr = config.ConfigReader(control_sum_filename, check_crc=False)
    for cs_from_file, filename_ext in cr.read(swtrans.str_start_files_header):
        # декодирую экранированные имена файлов (табуляция и обратный слэш)!
        full_file_name = f"{fld}{os.path.sep}{my_utils.unescape_file_name(filename_ext)}"
        yield full_file_name, cs_from_file


def check_files(control_sum_filename: str) -> tuple:
    """comparison of the current checksum of the file and the checksum read from the file."""
    # вызов my_utils.settings_from_file проверяет контрольную сумму файла настроек после его открытия
    settings = my_utils.settings_from_file(control_sum_filename, check_crc=True)
    if not settings:
        # ошибка доступа к файлу: settings_from_file уже напечатал сообщение об ошибке
        raise ValueError(f"{my_strings.strInvalidCheckFn}: {control_sum_filename}")
    for required_key in ("src", "alg"):
        if required_key not in settings:
            raise ValueError(f"{my_strings.strInvalidCheckFn}: missing '{required_key}' in {control_sum_filename}")
    total_tested, modified_files_count, access_errors, total_size = 0, 0, 0, 0
    for loc_fn, old_cs in parse_control_sum_file(control_sum_filename, settings):
        try:
            curr_cs = my_utils.get_hash_file(full_path_to_file=loc_fn, algorithm=settings['alg'])
            # вычисляю общий размер проверенных файлов в байтах
            total_size += my_utils.get_file_stat(loc_fn).st_size
            total_tested += 1
            if curr_cs != old_cs:
                modified_files_count += 1
                # сообщаю пользователю, что файл был проверен, изменения в файле ЕСТЬ!
                print(f"{my_strings.strFileModified}{swtrans.strKeyValueSeparator} {loc_fn}")
            else:
                # сообщаю пользователю, что файл был проверен, изменений в файле нет!
                print(f"{my_strings.strFileChecked}: {loc_fn}")
        except OSError as e:
            access_errors += 1
            print(e)
            continue

    return total_tested, modified_files_count, access_errors, total_size


def main():
    """Главная функция"""
    # изменяю кодировку stdout
    sys.stdout.reconfigure(encoding=config.Config.default_encoding)
    # Папка с файлами для подсчета их КС: по умолчанию это текущий рабочий каталог (см. README)!
    src_folder = os.getcwd()

    parser = argparse.ArgumentParser(description=my_strings.strDescription, epilog=my_strings.strEpilog)
    # Что вообще такое %(prog)s?
    # %(prog)s — это заглушка, которую понимает только argparse. Когда пользователь пишет cfcs --version, 
    # библиотека argparse сама заменяет %(prog)s на имя, под которым запустили программу.
    # По умолчанию это os.path.basename(sys.argv[0]). То есть:
    # Если запустить как python -m calc_files_control_sum.cfcs, то prog будет cfcs.py.
    # Если через установленную команду cfcs — то prog будет просто cfcs.
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-c", "--check_file", type=str, help=my_strings.strArgCheckFile)
    parser.add_argument("-s", "--src", type=str, help=my_strings.strArgSrc)
    parser.add_argument("-a", "--alg", type=str, help=my_strings.strArgAlg, default="md5")
    parser.add_argument("-e", "--ext", type=str, help=my_strings.strArgExt, default="*.zip")

    args = parser.parse_args()

    # проверяю заданный алгоритм хеширования на существование в hashlib.
    if args.alg.lower() not in hashlib.algorithms_available:
        parser.error(f"Invalid checksum algorithm: {args.alg}")

    # режим проверки файлов включен (!= None)
    if args.check_file and not my_utils.is_file_exist(args.check_file):
        parser.error(f"{my_strings.strInvalidCheckFn}: {args.check_file}")

    if args.check_file:
        print(my_strings.strCheckingStarted)
        # текущее время
        dt = my_utils.DeltaTime()
        try:
            # проверка файлов по их контрольным суммам
            total_files, modified, access_err, total_size = check_files(args.check_file)
        except (OSError, ValueError) as e:
            # повреждённый/недоступный файл контроля или ошибка при проверке
            print(e)
            sys.exit(1)
        delta = dt.delta()  # in second [float]
        mib_per_sec = my_utils.calc_mib_per_sec(total_size, delta)
        # Итоги проверки файлов по их контрольным суммам
        print(f"{my_strings.strTotalFilesChecked}: {total_files}")
        print(f"{my_strings.strTotalFilesMod}: {modified}")
        print(f"{my_strings.strIOErrors}: {access_err}")
        print(f"{my_strings.strCheckingSpeed}: {mib_per_sec:.3f}")
        sys.exit()  # выход

    if args.src:
        if not my_utils.is_folder_exist(args.src):
            parser.error(f"{my_strings.strInvalidSrcFld} {args.src}")
    else:
        args.src = src_folder

    # формирование списка расширений для записи в секцию настроек файла
    args.ext = args.ext.replace(" ", "")   # удаляю все пробелы из строки
    args.ext = args.ext.split(",")  # создаю список
    # отбрасываю пустые части (от ввода "" или вида "*.zip, *.rar"!)
    args.ext = [pattern for pattern in args.ext if pattern]

    # текущее время
    dt = my_utils.DeltaTime()
    # добавляю в словарь время
    loc_d = vars(args)
    loc_d["start_time"] = str(dt.start_time)

    # сохраняю настройки в stdout
    cw = config.ConfigWriter(filename_or_fileobject=sys.stdout, check_crc=True)
    cw.write_section(swtrans.str_settings_header, loc_d.items())

    total_size = count_files = 0
    # вывод в stdout информации при подсчете контрольных сумм
    cw.write_section(swtrans.str_start_files_header, None)
    for file_hash, file_name, file_size in process(args.src, args.ext, args.alg):
        total_size += file_size  # file size
        count_files += 1
        # имя файла экранирую: табуляция - разделитель полей строки отчёта!
        cw.write_line(f"{file_hash}{swtrans.strCS_filename_splitter}{my_utils.escape_file_name(file_name)}")

    cw.write_section(swtrans.str_info_section, None)
    delta = dt.delta()  # in second [float]
    # строки файла отчёта (*.cs) не локализуются: формат одинаков во всех локалях
    cw.write_line(f"{swtrans.str_ended_report}: {dt.stop_time}\t"
                  f"{swtrans.str_files_report}: {count_files};\t"
                  f"{swtrans.str_bytes_processed_report}: {total_size}")
    mib_per_sec = my_utils.calc_mib_per_sec(total_size, delta)
    cw.write_line(f"{swtrans.str_proc_speed_report}: {mib_per_sec:.3f}")
    # явная запись строки CRC и завершение записи.
    cw.close()


if __name__ == '__main__':
    main()
