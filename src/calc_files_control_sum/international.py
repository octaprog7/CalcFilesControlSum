"""поддержка интернационализации"""
import locale

# 1	Китайский	    1 296 461 000[2] — 1 311 000 000	Китай	39
# 2	Испанский	    460 000 000	                        Испания	31
# 3	Английский	    379 000 000	                        Великобритания	137
# 4	Хинди	        341 000 000	                        Индия	4
# 5 Арабский	    315 421 300[3] — 319 000 000	    Саудовская Аравия	59
# 6	Бенгальский	    228 000 000	                        Бангладеш	4
# 7	Португальский	221 000 000	                        Португалия	15
# 8	Русский	        154 000 000	                        Россия	19
# 9	Японский	    128 000 000	                        Япония	2
'''
    'bg_BG': 'Bulgarian',
    'cs_CZ': 'Czech',
    'da_DK': 'Danish',
    'de_DE': 'German',
    'el_GR': 'Greek',
    'en_US': 'English',
    'es_ES': 'Spanish',
    'et_EE': 'Estonian',
    'fi_FI': 'Finnish',
    'fr_FR': 'French',
    'hr_HR': 'Croatian',
    'hu_HU': 'Hungarian',
    'it_IT': 'Italian',
    'lt_LT': 'Lithuanian',
    'lv_LV': 'Latvian',
    'nl_NL': 'Dutch',
    'no_NO': 'Norwegian',
    'pl_PL': 'Polish',
    'pt_PT': 'Portuguese',
    'ro_RO': 'Romanian',
    'ru_RU': 'Russian',
    'sk_SK': 'Slovak',
    'sl_SI': 'Slovenian',
    'sv_SE': 'Swedish',
    'tr_TR': 'Turkish',
    'zh_CN': 'Chinese',
'''

def _get_default_lang_code() -> str:
    """Смотри: https://docs.python.org/3/library/locale.html"""
    return locale.getdefaultlocale()[0]


def import_strings():
    lang = _get_default_lang_code()
    if "ru_RU" == lang:
        import calc_files_control_sum.my_strings_ru as my_strings
        return
    # default import EN lang module!
    import calc_files_control_sum.my_strings as my_strings