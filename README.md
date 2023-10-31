# CleanPhi

[![Downloads](https://static.pepy.tech/badge/cleanphi)](https://pepy.tech/project/cleanphi)

CleanPhi is a powerful Python framework designed to enhance text processing by effectively removing unwanted elements such as extraneous characters and unicodes. Leveraging the capabilities of natural language processing, CleanPhi provides a comprehensive set of functionalities, making it an invaluable tool for text cleaning and related tasks.

```python
from CleanPhi import clean

clean("some input",
    unicode=True,               # fix various unicode errors
    to_ascii=True,                  # transliterate to closest ASCII representation
    to_lower=True,                     # to_lowercase text
    no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
    remove_url=False,                  # replace all URLs with a special token
    remove_email=False,                # replace all email addresses with a special token
    remove_ph=False,         # replace all phone numbers with a special token
    remove_nums=False,               # replace all numbers with a special token
    remove_digits=False,                # replace all digits with a special token
    remove_currency=False,      # replace all currency symbols with a special token
    remove_punct=False,                 # remove punctuations
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
import CleanPhi
text = "Hello, world!  Hello...\t \tworld?\n\nHello:\r\n\n\nWorld. "
proc_text = "Hello, world! Hello... world?\nHello:\nWorld."
assert CleanPhi.remove_whitespace(text, no_line_breaks=False) == proc_text
assert CleanPhi.remove_whitespace(" dd\nd  ", no_line_breaks=True) == "dd d"
```

### To install CleanPhi in >=Python3.6

```powershell
pip install CleanPhi
```

### Use CleanPhi with Scikit

```python
from CleanPhi.scikit import PhiTransformer

cleaner = PhiTransformer(remove_punct=False, to_lower=False)
cleaner.transform(['Clean text.', 'Natural language processing!'])
```

# Version 0.2.0 

- Bugs fixed
