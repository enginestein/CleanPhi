from typing import Any, List, Union

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from .main import clean


class PhiTransformer(TransformerMixin, BaseEstimator):
    def __init__(
        self,
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
        self.unicode = unicode
        self.to_ascii = to_ascii
        self.to_lower = to_lower
        self.remove_whitespace = remove_whitespace
        self.no_line_breaks = no_line_breaks
        self.strip_lines = strip_lines
        self.keep_two_line_breaks = keep_two_line_breaks
        self.remove_url = remove_url
        self.remove_email = remove_email
        self.remove_ph = remove_ph
        self.remove_nums = remove_nums
        self.remove_digits = remove_digits
        self.remove_currency = remove_currency
        self.remove_punct = remove_punct
        self.remove_emoji = remove_emoji
        self.replace_with_url = replace_with_url
        self.replace_with_email = replace_with_email
        self.replace_with_phone_number = replace_with_phone_number
        self.replace_with_number = replace_with_number
        self.replace_with_digit = replace_with_digit
        self.replace_with_currency_symbol = replace_with_currency_symbol
        self.replace_with_punct = replace_with_punct
        self.lang = lang

    def fit(self, X: Any):
        return self

    def transform(self, X: Union[List[str], pd.Series]) -> Union[List[str], pd.Series]:
        if not (isinstance(X, list) or isinstance(X, pd.Series)):
            raise ValueError("The input must be a list or pd.Series")
        if isinstance(X, pd.Series):
            return X.apply(lambda text: clean(text, **self.get_params()))
        else:
            return list(map(lambda text: clean(text, **self.get_params()), X))
