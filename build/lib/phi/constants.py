import re
import sys
import unicodedata

CURRENCIES = {
    "$": "USD",
    "zł": "PLN",
    "£": "GBP",
    "¥": "JPY",
    "฿": "THB",
    "₡": "CRC",
    "₦": "NGN",
    "₩": "KRW",
    "₪": "ILS",
    "₫": "VND",
    "€": "EUR",
    "₱": "PHP",
    "₲": "PYG",
    "₴": "UAH",
    "₹": "INR",
}
CURRENCY_REGEX = re.compile(
    "({})+".format("|".join(re.escape(c) for c in CURRENCIES.keys()))
)

PUNCT_TRANSLATE_UNICODE = dict.fromkeys(
    (i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P")),
    "",
)

ACRONYM_REGEX = re.compile(
    r"(?:^|(?<=\W))(?:(?:(?:(?:[A-Z]\.?)+[a-z0-9&/-]?)+(?:[A-Z][s.]?|[0-9]s?))|(?:[0-9](?:\-?[A-Z])+))(?:$|(?=\W))",
    flags=re.UNICODE,
)

EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-](@|[(<{\[]at[)>}\]])(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))",
    flags=re.IGNORECASE | re.UNICODE,
)

PHONE_REGEX = re.compile(
    r"((?:^|(?<=[^\w)]))(((\+?[01])|(\+\d{2}))[ .-]?)?(\(?\d{3,4}\)?/?[ .-]?)?(\d{3}[ .-]?\d{4})(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W)))|\+?\d{4,5}[ .-/]\d{6,9}"
)

NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))"
)

LINEBREAK_REGEX = re.compile(r"((\r\n)|[\n\v])+")
TWO_LINEBREAK_REGEX = re.compile(r"((\r\n)|[\n\v])+((\r\n)|[\n\v])+")
MULTI_WHITESPACE_TO_ONE_REGEX = re.compile(r"\s+")
NONBREAKING_SPACE_REGEX = re.compile(r"(?!\n)\s+")

URL_REGEX = re.compile(
    r"(?:^|(?<![\w\/\.]))"
    r"(?:(?:https?:\/\/|ftp:\/\/|www\d{0,3}\.))"
    r"(?:\S+(?::\S*)?@)?" r"(?:"
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    r"(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)"
    r"(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*"
    r"(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))" r"|" r"(?:(localhost))" r")"
    r"(?::\d{2,5})?"
    r"(?:\/[^\)\]\}\s]*)?",
    flags=re.UNICODE | re.IGNORECASE,
)

strange_double_quotes = [
    "«",
    "‹",
    "»",
    "›",
    "„",
    "“",
    "‟",
    "”",
    "❝",
    "❞",
    "❮",
    "❯",
    "〝",
    "〞",
    "〟",
    "＂",
]

strange_single_quotes = ["‘", "‛", "’", "❛", "❜", "`", "´", "‘", "’"]

DOUBLE_QUOTE_REGEX = re.compile("|".join(strange_double_quotes))
SINGLE_QUOTE_REGEX = re.compile("|".join(strange_single_quotes))