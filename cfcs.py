#!/usr/bin/env python3
"""utility to calc files control sum in specified folder.

command string parameters:
first parameter:    source - folder where duplicates are searched.
second parameter:   algorithm - for calc control sum file (SHA1, SHA224, SHA256, SHA384,
 SHA512, MD5"""

import argparse
# import logging
import pathlib
import sys
import my_utils
import datetime
# import os


def process(full_path_to_folder: str, ext_list: list, alg: str):
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            if not ext_list or str(child.suffix) in ext_list:
                # file checksum calculation
                loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                yield loc_hash, child.name, child.stat().st_size


def check_files():
    print("Checking files under construction!!!")

if __name__ == '__main__':
    head_header = "#"
    str_start_files_header = f"{head_header}FILES{head_header}"
    str_end_files_header = str_start_files_header[::-1]
    # def_ext_check_file = ".cs"  # расширение файла с контрольными суммами по умолчанию
    src_folder = my_utils.get_owner_folder_path(sys.argv[0])  # папка с файлами
    algorithm = "md5"  # алгоритм подсчета
    extensions = None  # фильтр расширений
    check_file_name = None  # имя файла с контрольными суммами
    # if check == True, checking file operation enabled!
    # check_mode = False
    # default file name folder control sum info
    # def_cs_filename = src_folder.split(sep=os.path.sep)[-1]  # имя файла с контрольными суммами
    # if len(def_cs_filename) < 3:
    #     def_cs_filename = "folder.cs"
    # else:
    #     def_cs_filename += def_ext_check_file

    parser = argparse.ArgumentParser(description="utility to calc files control sum in specified folder.",
                                     epilog="""If the source folder is not specified, 
                                                current working directory used as source folder!""")

    parser.add_argument("--src", type=str, help="Folder in which checksums of files are calculated.")
    parser.add_argument("--alg", type=str, help="Algorithm for calculating the checksum. For example \
    md5 or sha256. Default value: md5")
    parser.add_argument("--ext", type=str, help='File extensions that will be subject to checksum calculation! \
    For example: ".zip,.rar,.txt"')
    parser.add_argument("--check_file", type=str, help="Name of the source file of checksums for checking files.")

    args = parser.parse_args()

    if args.check_file and my_utils.is_file_exist(args.check_file):
        check_file_name = args.check_file  # режим проверки файлов включен (!= None)

    if check_file_name:
        check_files()  # проверка файлов
        sys.exit()  # выход

    if args.src and my_utils.is_folder_exist(args.src):
        src_folder = args.src
    if args.alg:
        algorithm = args.alg
    if args.ext:
        extensions = args.ext.split(",")

    loc_now = datetime.datetime.now

    print(f"Folder handling: {src_folder}")
    extf = extensions
    if None is extf or not extf:
        extf = "none"
    print(f"File extension filter: {extf}")
    print(f"Checksum calculation algorithm: {algorithm}")
    print(f"Started: {loc_now()}\n")
    dt = my_utils.DeltaTime()
    total_size = count_files = 0
    #
    print(str_start_files_header)
    for item in process(src_folder, extensions, algorithm):
        total_size += item[2]  # file size
        count_files += 1
        print(f"{str(item[0]).upper()}\t{item[1]}")

    print(str_end_files_header)
    delta = dt.stop()
    print(f"\nEnded: {loc_now()}\nFiles: {count_files};\tBytes processed: {total_size}")
    mib_per_sec = total_size/(1024*1024)/delta
    print(f"Processing speed [MiB/sec]: {mib_per_sec}")
