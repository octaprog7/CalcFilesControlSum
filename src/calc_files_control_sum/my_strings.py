"""any strings for project"""
import os
import pathlib
import locale
import calc_files_control_sum.internationalization as my_int

# чтобы активировать пользовательскую locale! Для форматирования даты и времени!
# locale.setlocale(locale.LC_ALL, '')
# текущий язык локали
try:
    _loc_lang = locale.getlocale()[0]
except Exception:
    _loc_lang = None
if not _loc_lang:
    _loc_lang = os.environ.get("LC_ALL") or os.environ.get("LANG") or "en"
curr_lang = _loc_lang[:2].upper()
# полный путь к файлу
src_folder = pathlib.Path(__file__).parent
# чтение интернационализированных строк
_I = my_int.CSVProvider(f"{src_folder}{os.path.sep}translated.csv", "strID", curr_lang)

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

# для config.py
strInvalidInputParameter = _I("strInvalidInputParameter")
strInvalidCrcValue = _I("strInvalidCrcValue")
strCalcul = _I("strCalcul")
strInvalidSectionNameLength = _I("strInvalidSectionNameLength")

# для my_utils.py
strOsError = _I("strOsError")
strFileChecked = _I("strFileChecked")
