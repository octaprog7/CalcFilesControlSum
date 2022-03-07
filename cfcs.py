#!/usr/bin/env python3
"""utility to calc files control sum in specified folder.

command string parameters:
first parameter:    source - folder where duplicates are searched.
second parameter:   algorithm - for calc control sum file (SHA1, SHA224, SHA256, SHA384,
                                SHA512, MD5 """

import argparse
# import logging
import pathlib
import sys
import my_utils
import datetime


def process(full_path_to_folder: str, ext_list: list, alg: str):
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            if not ext_list or str(child.suffix) in ext_list:
                # file checksum calculation
                loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                yield loc_hash, child.name, alg


if __name__ == '__main__':
    src_folder = my_utils.get_owner_folder_path(sys.argv[0])
    algorithm = "md5"
    extensions = None

    parser = argparse.ArgumentParser(description="utility to calc files control sum in specified folder.",
                                     epilog="""If the source folder is not specified, 
                                                current working directory used as source folder!""")

    parser.add_argument("--src", type=str, help="Folder in which checksums of files are calculated.")
    parser.add_argument("--alg", type=str, help="Algorithm for calculating the checksum. For example \
    md5 or sha256. Default value: md5")
    parser.add_argument("--ext", type=str, help='File extensions that will be subject to checksum calculation! \
    For example: ".zip,.rar,.txt"')

    args = parser.parse_args()

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
    for item in process(src_folder, extensions, algorithm):
        print(f"{str(item[0]).upper()}\t{item[1]}")

    print(f"\nEnded: {loc_now()}")
