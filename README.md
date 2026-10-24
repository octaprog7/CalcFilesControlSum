# Utility to Calc Files Control Sum (CFCS) in specified folder.

File checksum information is written to stdout.
To later check the files for changes, you need to save this information
to a file by redirecting the output to a file (> filename.ext)

## Installation

On modern Linux distributions a plain `pip install ...` is blocked by default
(PEP 668 - "externally managed environment"), so install the utility with
[pipx](https://pipx.pypa.io/):

```bash
pipx install calc-files-control-sum
```

After installation the utility is available as the console command `cfcs`.
To upgrade: `pipx upgrade calc-files-control-sum`.

Alternative install options:
- into a virtual environment: `python -m venv .venv && .venv/bin/pip install calc-files-control-sum`;
- force installation with pip (not recommended): `pip install --user --break-system-packages calc-files-control-sum`.

## Command string parameters:
  - -h, --help            show this help message and exit
  - --version             show program's version number and exit
  - -c CHECK_FILE, --check_file CHECK_FILE
                        Name of the source file of checksums for checking
                        files. Type: cfcs [opt] > filename.ext to produce
                        check file filename.ext in current working dir!
  - -s SRC, --src SRC     Folder in which checksums of files are calculated.
  - -a ALG, --alg ALG     Algorithm for calculating the checksum. For example
                        MD5, SHA1, SHA224, SHA256, SHA384, SHA512. Default
                        value: md5
  - -e EXT, --ext EXT     Pattern string for filename matching check! Filters
                        out files subject to checksum calculation. For
                        example: "*.zip,*.rar,*.txt"
  
## Example: 
- ```cfcs --src=/home/username --alg=sha1 --ext="*.rar,*.avi,*.bmp" (writing checksum information to stdout).```
- ```cfcs --src=/home/username --alg=sha1 --ext="*.zip,*.7z,*.mp4" > control_sum_filename.ext (writing checksum information to file).```
- ```cfcs --check_file=/home/previously_created_file.ext  (check files in folder).```

## Make check folder file
    cfcs --src="/home/roman/Изображения" --ext="*.png" > my_images.cs
### Checking files for changes
    cfcs --check_file="my_images.cs"
## Work example
my_test.cs file content:
```
{SETTINGS}
check_file	None
src	/mnt/anydata/tmp
alg	md5
ext	['*.img']
start_time	2022-12-17 14:05:42.637208

{FILES_AND_CONTROL_SUM}
A981130CF2B7E09F4686DC273CF7187E	test1.img
CD573CFAACE07E7949BC0C46028904FF	test5.img
CD573CFAACE07E7949BC0C46028904FF	test3.img
CD573CFAACE07E7949BC0C46028904FF	test0.img
C698C87FB53058D493492B61F4C74189	test2.img
CD573CFAACE07E7949BC0C46028904FF	test4.img
{INFO AND STATISTICS}
Work completed: 2022-12-17 14:05:58.980157	Number of files: 6;	Bytes processed: 9663676416
Processing speed [MiB/s]: 563.913
hash_val	DD44D3D71819D7EE6A5622544AE1905E
```

## Checking files for changes
    cfcs --check_file="my_test.cs"

### Result
```
Checking files by their checksums has begun!
The file has been verified. No changes found.: /mnt/anydata/big_archive.tar.gz
Total files checked: 1
Number of modified files: 0
Number of I/O errors: 0
File scan speed [MiB/s]: 82.969
```
## PyPi
https://pypi.org/project/calc-files-control-sum/

## Internationalization
Most of the program messages are translated into five languages: English, Russian, German, Spanish, French.
See: https://github.com/octaprog7/PyInternalization.

## Note
- The folder scan is **NOT recursive**: only files directly located in the specified folder (top level) are
  processed. Files in subfolders are ignored by design.
- If you liked my software, please be generous and give it a star!