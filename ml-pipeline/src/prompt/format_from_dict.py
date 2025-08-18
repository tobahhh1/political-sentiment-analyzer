import re

def format_from_dict(d: dict, format: str):
    """
    Formats a string, replacing e.g. {{key}} with d["key"]
    Args:
        d: Dictionary to perform substitution from
        format: Format string, like "This will have the value d["key"]: ${key}"
    """
    replace_regex = r'(\{\{(.*?)\}\})' 
    matches = re.findall(replace_regex, format)
    for to_replace, key in matches:
        assert key in d, f"Invalid format string {format}: Unrecognized key {key}"
        format = format.replace(to_replace, d[key], 1)
    return format

