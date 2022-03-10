#!/usr/bin/env python3
"""utility to calc files control sum in specified folder.

command string parameters:
first parameter:    source - folder where duplicates are searched.
second parameter:   algorithm - for calc control sum file (SHA1, SHA224, SHA256, SHA384,
 SHA512, MD5"""

import argparse
import pathlib
import sys
import my_utils
import datetime
import my_strings
import json
import os


def process(full_path_to_folder: str, ext_list: list, alg: str):
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            if not ext_list or str(child.suffix) in ext_list:
                # file checksum calculation
                loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                yield loc_hash, child.name, child.stat().st_size


# разбор файла на имена файлов и их контрольные суммы!
def parse_files_info(control_sum_filename: str, settings: dict):
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

            two_sub_lines = line.split(my_strings.strCS_filename_splitter)
            full_file_name = f"{fld}{os.path.sep}{two_sub_lines[1].strip()}"
            cs = bytes(two_sub_lines[0].strip(), encoding="utf-8")

            yield full_file_name, cs.decode("utf-8").upper()


def check_files(control_sum_filename: str):
    print("Checking files under construction!!!")
    head = my_utils.load_settings_head_from_file(control_sum_filename)
    settings = json.loads(head)
    for itm in parse_files_info(control_sum_filename, settings):
        loc_cs = my_utils.get_hash_file(itm[0])
        if isinstance(loc_cs, str):
            loc_cs = loc_cs.upper()
        # print(itm[1], loc_cs)
        if loc_cs == itm[1]:
            print(f"{itm[0]}:\tOK")


if __name__ == '__main__':
    # def_ext_check_file = ".cs"  # расширение файла с контрольными суммами по умолчанию
    src_folder = my_utils.get_owner_folder_path(sys.argv[0])  # папка с файлами
    def_algorithm = "md5"  # алгоритм подсчета
    extensions = None  # фильтр расширений
    check_file_name = None  # имя файла с контрольными суммами

    parser = argparse.ArgumentParser(description="utility to calc files control sum in specified folder.",
                                     epilog="""If the source folder is not specified, 
                                                current working directory used as source folder!""")

    parser.add_argument("--check_file", type=str, help="Name of the source file of checksums for checking files.\
        Type: cfcs [opt] > filename.ext to produce check file filename.ext in current working dir!")
    parser.add_argument("--src", type=str, help="Folder in which checksums of files are calculated.")
    parser.add_argument("--alg", type=str, help="Algorithm for calculating the checksum. For example \
    md5 or sha256. Default value: md5", default="md5")
    parser.add_argument("--ext", type=str, help='File extensions that will be subject to checksum calculation! \
    For example: ".zip,.rar,.txt"', default="")

    args = parser.parse_args()

    # режим проверки файлов включен (!= None)
    if args.check_file and not my_utils.is_file_exist(args.check_file):
        raise ValueError(f"{my_strings.strInvalidCheckFn}: {args.check_file}")

    if args.check_file:
        check_files(args.check_file)  # проверка файлов
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

    # save settings to stream
    json.dump(obj=vars(args), fp=sys.stdout, indent=4)

    loc_now = datetime.datetime.now

    dt = my_utils.DeltaTime()
    total_size = count_files = 0
    #
    print(f"\n{my_strings.str_start_files_header}")
    for item in process(args.src, args.ext, args.alg):
        total_size += item[2]  # file size
        count_files += 1
        print(f"{str(item[0]).upper()}{my_strings.strCS_filename_splitter}{item[1]}")

    print(my_strings.str_end_files_header)
    delta = dt.stop()
    print(f"\nEnded: {loc_now()}\nFiles: {count_files};\tBytes processed: {total_size}")
    mib_per_sec = total_size/(1024*1024)/delta
    print(f"Processing speed [MiB/sec]: {mib_per_sec}")
