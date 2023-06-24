# Phi

Phi is a powerful Python framework designed to enhance text processing by effectively removing unwanted elements such as extraneous characters and unicodes. Leveraging the capabilities of natural language processing, Phi provides a comprehensive set of functionalities, making it an invaluable tool for text cleaning and related tasks.

```python
from cleantext import clean

clean("some input",
    fix_unicode=True,               # fix various unicode errors
    to_ascii=True,                  # transliterate to closest ASCII representation
    lower=True,                     # lowercase text
    no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
    no_urls=False,                  # replace all URLs with a special token
    no_emails=False,                # replace all email addresses with a special token
    no_phone_numbers=False,         # replace all phone numbers with a special token
    no_numbers=False,               # replace all numbers with a special token
    no_digits=False,                # replace all digits with a special token
    no_currency_symbols=False,      # replace all currency symbols with a special token
    no_punct=False,                 # remove punctuations
    replace_with_punct="",          # instead of removing punctuations you may replace them
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    lang="en"                       # set to 'de' for German special handling
)
```

Choose an arguement and use the **clean** function in your code:

```python
import phi
text = "Hello, world!  Hello...\t \tworld?\n\nHello:\r\n\n\nWorld. "
proc_text = "Hello, world! Hello... world?\nHello:\nWorld."
assert phi.normalize_whitespace(text, no_line_breaks=False) == proc_text
assert phi.normalize_whitespace(" dd\nd  ", no_line_breaks=True) == "dd d"
```

### To install Phi in >=Python3.6

```powershell
pip install phi
```

### Use Phi with Scikit

```python
from phi.scikit import PhiTransformer

cleaner = PhiTransformerr(no_punct=False, lower=False)
cleaner.transform(['Clean text.', 'Natural language processing!'])
```
