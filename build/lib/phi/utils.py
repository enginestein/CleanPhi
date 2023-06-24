def remove_substrings(text, to_replace, replace_with=""):
    if isinstance(to_replace, str):
        to_replace = [to_replace]

    result = text
    for x in to_replace:
        result = result.replace(x, replace_with)
    return result