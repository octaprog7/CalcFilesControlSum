Utility to calc files control sum in specified folder.

Command string parameters:
  --source - folder where duplicates are searched.
  --algorithm - for calc control sum file (SHA1, SHA224, SHA256, SHA384, SHA512, MD5 
  
Example: cfcs --src=/home/username --alg=sha1 --ext=".txt,.zip,.rar" (without storing checksum information)
         cfcs --src=/home/username --alg=sha1 --ext=".txt,.zip,.rar" > control_sum_filename.ext (with storing checksum information)
