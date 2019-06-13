"""son (sequential object notation) <https://github.com/flokno/son>"""

import warnings
from pathlib import Path

try:
    import ujson as json
except ModuleNotFoundError:
    import json

delim1 = "\n===\n"
delim2 = "\n---\n"


def dumps(obj, is_metadata=False, dumper=json.dumps, **kwargs):
    """dump an object to string representation

    Args:
        obj (Object): object to be dumped to string
        is_metadata (bool): if yes, delimit with === instead of ---
        dumper (encoder): e.g. json.dumps
        **kwargs: args to be passed to the dumper

    """

    rep = dumper(obj, **kwargs)

    if is_metadata:
        delimiter = delim1
    else:
        delimiter = delim2

    delimiter = "\n{}\n".format(delimiter)

    return rep + "{}".format(delimiter)


def dump(obj, file, is_metadata=False, **kwargs):
    """dump an object to son file. metadata can only be written once.

    Args:
        obj (Object): object to be dumped to string
        file (str or Path): file to dump to
        is_metadata (bool): if yes, delimit with === instead of ---
        **kwargs: args to be passed to son.dumps

    """

    rep = dumps(obj, is_metadata=is_metadata, **kwargs)

    if is_metadata:
        if Path(file).exists():
            msg = "{} exists, possibility of data loss!".format(file)
            raise FileExistsError(msg)

        with open(file, "w") as f:
            f.write(rep)

    else:
        with open(file, "a") as f:
            f.write(rep)


def loads(string, loader=json.loads, **kwargs):
    """decode string to object

    Args:
        string (str): the string to load
        loader (decoder): e.g. json.loads
        **kwargs: kwargs that get passed to the loader
    Returns:
        metadata, data: the loaded json blobs within the string

    """

    data = None
    metadata = None

    if string.strip() == "":
        msg = "Empty string was given, return None, None"
        warnings.warn(msg)
        return None, None

    try:
        raw_metadata, data_string = string.split(delim1)
        metadata = loader(raw_metadata, **kwargs)
    except ValueError:
        data_string = string

    raw_data = data_string.split(delim2)

    data = [loader(blob, **kwargs) for blob in raw_data if blob.strip()]

    return metadata, data


def load(file, **kwargs):
    """load and decode son file

    Args:
        file (path/str): load file
        kwargs: kwargs for son.loads

    Returns:
        metadata, data: content of file

    """

    with open(file) as fp:
        string = fp.read()
        if string.strip() == "":
            msg = "Empty string was given, return None, None"
            warnings.warn(msg)
            return None, None

        obj = loads(string, **kwargs)

    return obj
