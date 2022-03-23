Utility to Calc Files Control Sum (CFCS) in specified folder.

File checksum information is written to stdout.
To later check the files for changes, you need to save this information 
to a file by redirecting the output to a file (> filename.ext)

Command string parameters:
  - --src - the checksums of the files in this folder are calculated. Default - current working dir.
  - --alg - for calc control sum file (SHA1, SHA224, SHA256, SHA384, SHA512, MD5). Default - MD5
  - --ext - File name templates, according to which the checksum of the file will be calculated.
  - --check_file - Name of the source file of checksums for checking files. If this option is defined, then the rest do not need to be defined!
  
Example: 
- ```cfcs --src=/home/username --alg=sha1 --ext="*.rar,*.avi,*.bmp" (writing checksum information to stdout).```
- ```cfcs --src=/home/username --alg=sha1 --ext="*.zip,*.7z,*.mp4" > control_sum_filename.ext (writing checksum information to file).```
- ```cfcs --check_file==/home/previously_created_file.ext  (check files in folder).```
