"""son.serialize

The serialization interface for son, defining how objects
are turned into strings, and vice-versa. The dumper and
loader are expected to be callables with arbitrary keyword
arguments, which are simply passed through.

"""

import warnings

try:
    import ujson as json
except ModuleNotFoundError:
    import json


def dump(obj, dumper=json.dumps, **kwargs):
    return dumper(obj, **kwargs)


def load(string, loader=json.loads, **kwargs):

    if string.strip() == "":
        msg = "Empty string was given, return None"
        warnings.warn(msg)
        return None

    return loader(string, **kwargs)
