import logging
import re
import sys
from unicodedata import category

from emoji import UNICODE_EMOJI, demojize, emojize
from ftfy import fix_text

from . import constants
from .extra import save_replace
from .utils import remove_substrings

log = logging.getLogger()

try:
    from unidecode import unidecode

except ImportError:
    from unicodedata import normalize

    unidecode = lambda x: normalize("NFD", x).encode("ASCII", "ignore").decode("utf-8")
    log.warning(
        "Since the GPL-licensed package `unidecode` is not installed, using Python's `unicodedata` package which yields worse results."
    )


def fix_strange_quotes(text):
    text = constants.SINGLE_QUOTE_REGEX.sub("'", text)
    text = constants.DOUBLE_QUOTE_REGEX.sub('"', text)
    return text


def fix_bad_unicode(text, normalization="NFC"):
    try:
        text = text.encode("latin", "backslashreplace").decode("unicode-escape")
    except:
        pass

    return fix_text(text, normalization=normalization)


def to_ascii_unicode(text, lang="en", no_emoji=False):
    text = fix_strange_quotes(text)

    if not no_emoji:
        text = demojize(text, use_aliases=True)

    lang = lang.lower()
    if lang == "de":
        text = save_replace(text, lang=lang)

    text = unidecode(text)
    
    if lang == "de":
        text = save_replace(text, lang=lang, back=True)

    if not no_emoji:
        text = emojize(text, use_aliases=True)

    return text


def normalize_whitespace(
    text, no_line_breaks=False, strip_lines=True, keep_two_line_breaks=False
):

    if strip_lines:
        text = "\n".join([x.strip() for x in text.splitlines()])

    if no_line_breaks:
        text = constants.MULTI_WHITESPACE_TO_ONE_REGEX.sub(" ", text)
    else:
        if keep_two_line_breaks:
            text = constants.NONBREAKING_SPACE_REGEX.sub(
                " ", constants.TWO_LINEBREAK_REGEX.sub(r"\n\n", text)
            )
        else:
            text = constants.NONBREAKING_SPACE_REGEX.sub(
                " ", constants.LINEBREAK_REGEX.sub(r"\n", text)
            )

    return text.strip()

def _normalize_whitespace(*kwargs):
    return normalize_whitespace(*kwargs)


def replace_urls(text, replace_with="<URL>"):
    return constants.URL_REGEX.sub(replace_with, text)


def replace_emails(text, replace_with="<EMAIL>"):
    return constants.EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with="<PHONE>"):
    return constants.PHONE_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with="<NUMBER>"):
    return constants.NUMBERS_REGEX.sub(replace_with, text)


def replace_digits(text, replace_with="0"):
    return re.sub(r"\d", replace_with, text)


def replace_currency_symbols(text, replace_with="<CUR>"):
    if replace_with is None:
        for k, v in constants.CURRENCIES.items():
            text = text.replace(k, v)
        return text
    else:
        return constants.CURRENCY_REGEX.sub(replace_with, text)


def replace_punct(text, replace_with=" "):
    return text.translate(
        dict.fromkeys(
            (i for i in range(sys.maxunicode) if category(chr(i)).startswith("P")),
            replace_with,
        )
    )


def remove_punct(text):
    return text.translate(constants.PUNCT_TRANSLATE_UNICODE)


def remove_emoji(text):
    return remove_substrings(text, UNICODE_EMOJI["en"])


def clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    normalize_whitespace=True,
    no_line_breaks=False,
    strip_lines=True,
    keep_two_line_breaks=False,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_numbers=False,
    no_digits=False,
    no_currency_symbols=False,
    no_punct=False,
    no_emoji=False,
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    replace_with_punct="",
    lang="en",
):
    if text is None:
        return ""

    text = str(text)

    if fix_unicode:
        text = fix_bad_unicode(text)
    if no_currency_symbols:
        text = replace_currency_symbols(text, replace_with_currency_symbol)
    if to_ascii:
        text = to_ascii_unicode(text, lang=lang, no_emoji=no_emoji)
    if no_urls:
        text = replace_urls(text, replace_with_url)
    if no_emails:
        text = replace_emails(text, replace_with_email)
    if no_phone_numbers:
        text = replace_phone_numbers(text, replace_with_phone_number)
    if no_numbers:
        text = replace_numbers(text, replace_with_number)
    if no_digits:
        text = replace_digits(text, replace_with_digit)
    if no_punct:
        if replace_with_punct == "":
            text = remove_punct(text)
        else:
            text = replace_punct(text, replace_with_punct)

    if no_emoji and not to_ascii:
        text = remove_emoji(text)

    if lower:
        text = text.lower()

    if normalize_whitespace:
        text = _normalize_whitespace(
            text, no_line_breaks, strip_lines, keep_two_line_breaks
        )

    return text