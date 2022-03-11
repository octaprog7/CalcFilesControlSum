Utility to calc files control sum in specified folder.

Command string parameters:
  --src - folder where duplicates are searched.
  --alg - for calc control sum file (SHA1, SHA224, SHA256, SHA384, SHA512, MD5 
  --ext - file extensions that will be subject to checksum calculation. For example: ".zip,.rar,.txt"
  --check_file - Name of the source file of checksums for checking files
  
Example: cfcs --src=/home/username --alg=sha1 --ext=".txt,.zip,.rar" (without storing checksum information)
         cfcs --src=/home/username --alg=sha1 --ext=".txt,.zip,.rar" > control_sum_filename.ext (with storing checksum information)
