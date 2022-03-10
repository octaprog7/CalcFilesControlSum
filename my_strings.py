"""any strings for util"""

strFolderHandling = "Folder handling"
strFEF = "File extension filter"
strCCA = "Checksum calculation algorithm"

head_header = "#"
str_start_files_header = f"{head_header}FILES{head_header}"
str_end_files_header = str_start_files_header[::-1]
strCS_filename_splitter = "\t"
strKeyValueSeparator = ":"

ParsingKeys = (
    strFolderHandling,
    strFEF,
    strCCA
)

strInvalidSrcFld = "Invalid source folder!"
strInvalidCheckFn = "Invalid check file name!"
strOsError = "Operational System Error!"






#def store_settings(folder: str, extension_filter: str, algorithm: str) -> dict:
#    res = dict()
#    res[strFolderHandling] = folder
#    res[strFEF] = extension_filter
#    res[strCCA] = algorithm
#    return res
