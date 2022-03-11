#!/usr/bin/env python3
"""service utils"""

import hashlib
import pathlib
import datetime
import my_strings
import io


# def get_hash_file(full_path_to_file: str, algorithm="md5", buff_size=4096, as_hex_digest=True):
def get_hash_file(full_path_to_file: str, algorithm="md5", buff_size=4096):
    """return hash of file"""
    h = hashlib.new(algorithm)
    with open(full_path_to_file, "rb") as f:
        for chunk in iter(lambda: f.read(buff_size), b""):
            h.update(chunk)

    # if as_hex_digest:
    return h.hexdigest()
    # return h.digest()


def is_folder_exist(full_folder_path: str) -> bool:
    """check folder for exist and is folder
    return value is Boolean!"""
    folder = pathlib.Path(full_folder_path)
    return folder.is_dir() and folder.exists()


def is_file_exist(filename: str) -> bool:
    """check file for exist"""
    p = pathlib.Path(filename)
    return p.is_file()


def get_owner_folder_path(full_path_to_file: str) -> str:
    """ return owner folder path from full path file name """
    mypath = pathlib.Path(full_path_to_file).absolute()
    return str(mypath.parent)


def get_file_name_from_path(full_path_to_file: str) -> str:
    """ return filename from full path file name """
    path = pathlib.Path(full_path_to_file)
    return path.name


def get_file_extension_from_path(full_path_to_file: str) -> str:
    """ return file extension from full path file name """
    path = pathlib.Path(full_path_to_file)
    return path.suffix


def split_path(full_path_to_file: str) -> tuple:
    """Divides the file path into three parts: parent (owner folder name), name (file name), suffix(ext)"""
    path = pathlib.Path(full_path_to_file)
    return str(path.parent), path.name, path.suffix


class DeltaTime:
    """time interval measurement"""
    @staticmethod
    def get_time() -> datetime.datetime:
        """return time in second"""
        return datetime.datetime.now()

    def __init__(self):
        self._start = DeltaTime.get_time()
        self._stop = None

    def start(self):
        """call start before measurement"""
        self.__init__()

    def delta(self) -> float:
        """return delta time in second"""
        self._stop = DeltaTime.get_time()
        dt = self._stop.timestamp() - self._start.timestamp()
        return dt

    def get_start_stop(self):
        return self._start, self._stop

def load_settings_head_from_file(filename: str) -> str:
    f_ram = io.StringIO()
    try:
        # create file in RAM
        with open(file=filename, encoding="utf-8") as fp:
            for line in fp:
                if line.startswith(my_strings.str_start_files_header):
                    break  # exit, files section!
                f_ram.write(line)
    except OSError as e:
        print(f"{my_strings.strOsError}: {e}")
    finally:
        s = f_ram.getvalue()
        f_ram.close()
    return s
