"""any strings for project"""

# переводимые на другие языки строки

# для cfcs.py                EN
strInvalidSrcFld = "Invalid source folder!"             # used in cfcs.py
strInvalidCheckFn = "Invalid name of check file!"          # used in cfcs.py
strFileModified = "Attention! The file has been modified"   # used in cfcs.py
strCheckingStarted = "Checking started!"                    # used in cfcs.py

strDescription = "Utility to Calc Files Control Sum in specified folder."   # used in cfcs.py
strEpilog = "If the source folder is not specified, current working directory used as source folder!"  # used in cfcs.py
strArgCheckFile = "Name of the source file of checksums for checking files.\
            Type: cfcs [opt] > filename.ext to produce check file filename.ext in current working dir!"  # u in  cfcs.py
strArgSrc = "Folder in which checksums of files are calculated."    # used in cfcs.py
strArgAlg = "Algorithm for calculating the checksum. For example \
        MD5, SHA1, SHA224, SHA256, SHA384, SHA512. Default value: md5"  # used in cfcs.py
strArgExt = 'Pattern string for filename matching check! \
        Filters out files subject to checksum calculation. For example: "*.zip,*.rar,*.txt"'    # used in cfcs.py

# для cfcs.py
strCheckingSpeed = "Checking speed [MiB/sec]"
strTotalFilesChecked = "Total files checked"
strTotalFilesMod = "Modified files"
strIOErrors = "I/O errors"
strProcSpeed = "Processing speed [MiB/sec]"
strEnded = "Ended"
strFiles = "Files"
strBytesProcessed = "Bytes processed"

# для config.py
strInvalidInputParameter = "Invalid input parameter"
strInvalidCrcValue = "File corrupt! Invalid CRC value! Read from file"
strCalcul = "calculated"
strInvalidSectionNameLength = "Invalid section name length!"

# для my_utils.py
strOsError = "Operational System Error!"                    # used in my_utils.py
