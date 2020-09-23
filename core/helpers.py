import re


def underscore(word):
    """
    >>> underscore("deviceType")
    'device_type'
    >>> underscore("DeviceType")
    'device_type'
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def camelize(string, uppercase_first_letter=False):
    """
    >>> camelize("device_type", True)
    'DeviceType'
    >>> camelize("device_type")
    'deviceType'
    """
    big = re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    if uppercase_first_letter:
        return big
    else:
        return big[0].lower() + big[1:]