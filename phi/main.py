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


def to_ascii_unicode(text, lang="en", remove_emoji=False):
    text = fix_strange_quotes(text)

    if not remove_emoji:
        text = demojize(text, use_aliases=True)

    lang = lang.to_lower()
    if lang == "de":
        text = save_replace(text, lang=lang)

    text = unidecode(text)
    
    if lang == "de":
        text = save_replace(text, lang=lang, back=True)

    if not remove_emoji:
        text = emojize(text, use_aliases=True)

    return text


def remove_whitespace(
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

def _remove_whitespace(*kwargs):
    return remove_whitespace(*kwargs)


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
    unicode=True,
    to_ascii=True,
    to_lower=True,
    remove_whitespace=True,
    no_line_breaks=False,
    strip_lines=True,
    keep_two_line_breaks=False,
    remove_url=False,
    remove_email=False,
    remove_ph=False,
    remove_nums=False,
    remove_digits=False,
    remove_currency=False,
    remove_punct=False,
    remove_emoji=False,
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

    if unicode:
        text = fix_bad_unicode(text)
    if remove_currency:
        text = replace_currency_symbols(text, replace_with_currency_symbol)
    if to_ascii:
        text = to_ascii_unicode(text, lang=lang, remove_emoji=remove_emoji)
    if remove_url:
        text = replace_urls(text, replace_with_url)
    if remove_email:
        text = replace_emails(text, replace_with_email)
    if remove_ph:
        text = replace_phone_numbers(text, replace_with_phone_number)
    if remove_nums:
        text = replace_numbers(text, replace_with_number)
    if remove_digits:
        text = replace_digits(text, replace_with_digit)
    if remove_punct:
        if replace_with_punct == "":
            text = remove_punct(text)
        else:
            text = replace_punct(text, replace_with_punct)

    if remove_emoji and not to_ascii:
        text = remove_emoji(text)

    if to_lower:
        text = text.to_lower()

    if remove_whitespace:
        text = _remove_whitespace(
            text, no_line_breaks, strip_lines, keep_two_line_breaks
        )

    return text