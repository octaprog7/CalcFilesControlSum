"""any strings for project"""
import os
import pathlib
import sys
import locale
import calc_files_control_sum.my_int as my_int

# чтобы активировать пользовательскую locale! Для форматирования даты и времени!
# locale.setlocale(locale.LC_ALL, '')
# текущий язык локали
curr_lang = locale.getdefaultlocale()[0][:2].upper()
# полный путь к файлу
src_folder = pathlib.Path(sys.argv[0]).parent
# чтение интернационализированных строк
_I = my_int.Internationalization(f"{src_folder}{os.path.sep}translated.csv", curr_lang)

# переводимые на другие языки строки

# для cfcs.py
strInvalidSrcFld = _I("strInvalidSrcFld")               # used in cfcs.py
strInvalidCheckFn = _I("strInvalidCheckFn")             # used in cfcs.py
strFileModified = _I("strFileModified")                 # used in cfcs.py
strCheckingStarted = _I("strCheckingStarted")           # used in cfcs.py

strDescription = _I("strDescription")   # used in cfcs.py
strEpilog = _I("strEpilog")             # used in cfcs.py
strArgCheckFile = _I("strArgCheckFile")        # used in  cfcs.py
strArgSrc = _I("strArgSrc")     # used in cfcs.py
strArgAlg = _I("strArgAlg")     # used in cfcs.py
strArgExt = _I("strArgExt")     # used in cfcs.py

# для cfcs.py
strCheckingSpeed = _I("strCheckingSpeed")
strTotalFilesChecked = _I("strTotalFilesChecked")
strTotalFilesMod = _I("strTotalFilesMod")
strIOErrors = _I("strIOErrors")
strProcSpeed = _I("strProcSpeed")
strEnded = _I("strEnded")
strFiles = _I("strFiles")
strBytesProcessed = _I("strBytesProcessed")

# для config.py
strInvalidInputParameter = _I("strInvalidInputParameter")
strInvalidCrcValue = _I("strInvalidCrcValue")
strCalcul = _I("strCalcul")
strInvalidSectionNameLength = _I("strInvalidSectionNameLength")

# для my_utils.py
strOsError = _I("strOsError")
