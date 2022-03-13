**Utility to Calc Files Control Sum (CFCS) in specified folder.**

**Command string parameters:**
  - --src - the checksums of the files in this folder are calculated.
  - --alg - for calc control sum file (SHA1, SHA224, SHA256, SHA384, SHA512, MD5.
  - --ext - File name templates, according to which the checksum of the file will be calculated. For example: ".zip,.rar,.txt".
  - --check_file - Name of the source file of checksums for checking files. If this option is defined, then the rest do not need to be defined!
  
**Example:** 
- cfcs --src=/home/username --alg=sha1 --ext="*.txt,*.zip,*.rar" (writing checksum information to stdout).
- cfcs --src=/home/username --alg=sha1 --ext="*.txt,*.zip,*.rar" > control_sum_filename.ext (with storing checksum information).
