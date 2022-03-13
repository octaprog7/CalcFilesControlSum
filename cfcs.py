#!/usr/bin/env python3
"""Utility to calc files control sum in specified folder.
    Type --help for command line parameters description."""

import argparse
import pathlib
import sys
import my_utils
import my_strings
import fnmatch
import json
import os


def process(full_path_to_folder: str, ext_list: list, alg: str) -> tuple[str, str, int]:
    """Перечисляет файлы внутри папки, подсчитывая их контрольную сумму,
    получая имя файла и его размер в байтах.
    Функция-генератор"""
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            for pattern in ext_list:
                if fnmatch.fnmatch(child.name, pattern):
                    # file checksum calculation
                    loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                    yield loc_hash, child.name, child.stat().st_size
                    break


def parse_files_info(control_sum_filename: str, settings: dict) -> tuple[str, str]:
    """разбор файла на имена файлов и их контрольные суммы!
    Функция-генератор"""
    files_header_found = False
    # print(settings)
    fld = settings["src"]
    with open(control_sum_filename, "r", encoding="utf-8") as f:
        for line in f:
            if not files_header_found:
                if not line.startswith(my_strings.str_start_files_header):
                    continue  # skip settings section!
                else:
                    files_header_found = True
                    continue
            if line.startswith(my_strings.str_end_files_header):
                break
            try:
                two_sub_lines = line.split(my_strings.strCS_filename_splitter)
                full_file_name = f"{fld}{os.path.sep}{two_sub_lines[1].strip()}"
                cs = bytes(two_sub_lines[0].strip(), encoding="utf-8")

                yield full_file_name, cs.decode("utf-8").upper()
            except Exception as e:
                print(my_strings.strParseFileError, control_sum_filename)
                print(e)


def check_files(control_sum_filename: str):
    """comparison of the current checksum of the file and the checksum read from the file.
    Функция-генератор"""
    print(my_strings.strCheckingStarted)
    head = my_utils.load_settings_head_from_file(control_sum_filename)
    settings = json.loads(head)
    total_tested, modified_files_count, access_errors = 0, 0, 0
    for loc_fn, old_cs in parse_files_info(control_sum_filename, settings):
        curr_cs = None
        try:
            curr_cs = my_utils.get_hash_file(loc_fn)
        except OSError as e:
            access_errors += 1
            print(e)
        total_tested += 1
        if curr_cs != old_cs:
            modified_files_count += 1
            print(f"{my_strings.strFileModified}{my_strings.strKeyValueSeparator} {loc_fn}")

    # Итоги проверки файлов по их контрольным суммам
    print(f"Total files checked: {total_tested}\tModified files: {modified_files_count}\tI/O errors: {access_errors}")


if __name__ == '__main__':
    """Главная функция"""
    src_folder = my_utils.get_owner_folder_path(sys.argv[0])  # папка с файлами
    def_algorithm = "md5"  # алгоритм подсчета
    extensions = None  # фильтр расширений
    check_file_name = None  # имя файла с контрольными суммами

    parser = argparse.ArgumentParser(description="utility to Calc Files Control Sum in specified folder.",
                                     epilog="""If the source folder is not specified, 
                                                current working directory used as source folder!""")

    parser.add_argument("--check_file", type=str, help="Name of the source file of checksums for checking files.\
        Type: cfcs [opt] > filename.ext to produce check file filename.ext in current working dir!")
    parser.add_argument("--src", type=str, help="Folder in which checksums of files are calculated.")
    parser.add_argument("--alg", type=str, help="Algorithm for calculating the checksum. For example \
    MD5, SHA1, SHA224, SHA256, SHA384, SHA512. Default value: md5", default="md5")
    parser.add_argument("--ext", type=str, help='Pattern string for filename matching check! \
    Filters out files subject to checksum calculation. For example: "*.zip,*.rar,*.txt"', default="*.*")

    args = parser.parse_args()

    # режим проверки файлов включен (!= None)
    if args.check_file and not my_utils.is_file_exist(args.check_file):
        raise ValueError(f"{my_strings.strInvalidCheckFn}: {args.check_file}")

    if args.check_file:
        check_files(args.check_file)  # проверка файлов по их контрольным суммам
        sys.exit()  # выход

    if args.src:
        if not my_utils.is_folder_exist(args.src):
            raise ValueError(f"{my_strings.strInvalidSrcFld}: {args.src}")
    else:
        args.src = src_folder

    if not args.alg:
        args.alg = def_algorithm

    if args.ext:
        loc_ext = args.ext.split(",")
        args.ext = loc_ext

    # текущее время
    dt = my_utils.DeltaTime()
    # добавляю в словарь время
    loc_d = vars(args)
    loc_d["start_time"] = str(dt.get_start_stop_times()[0])

    # сохраняю настройки в stdout в виде JSON
    json.dump(obj=loc_d, fp=sys.stdout, indent=4)
    total_size = count_files = 0
    # вывод в stdout информации при подсчете контрольных сумм
    print(f"\n{my_strings.str_start_files_header}")
    for file_hash, file_name, file_size in process(args.src, args.ext, args.alg):
        total_size += file_size  # file size
        count_files += 1
        print(f"{str(file_hash).upper()}{my_strings.strCS_filename_splitter}{file_name}")

    print(my_strings.str_end_files_header)
    delta = dt.delta()  # in second [float]
    print(f"\nEnded: {dt.get_start_stop_times()[1]}\nFiles: {count_files};\tBytes processed: {total_size}")
    mib_per_sec = total_size/(1024*1024)/delta
    print(f"Processing speed [MiB/sec]: {mib_per_sec}")
