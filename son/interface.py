"""son.interface

Defines the public-facing interface for son.

For performance reasons, son.open should be preferred over son.load.

"""

from pathlib import Path

import son.stream as stream
import son.serialize as serialize


def dump(obj, file, is_metadata=False, encoding="utf-8", **kwargs):
    """dump an object to son file, metadata can only be written once

    Args:
        obj (Object): object to be dumped to string
        file (str or Path): file to dump to
        is_metadata (bool): is this a metadata entry?
        encoding (optional, str): encoding to pass to open()
            defaults to "utf-8"
        **kwargs: args to be passed to son.serialize.dump
    """

    if is_metadata and Path(file).exists():
        msg = "{} exists, possibility of data loss!".format(file)
        raise FileExistsError(msg)

    string = serialize.dump(obj, **kwargs)

    with open(file, "a", encoding=encoding) as f:
        stream.write(f, string, is_metadata=is_metadata)


def load(file, verbose=False, encoding="utf-8", **kwargs):
    """load and decode son file

    Args:
        file (path/str): load file
        verbose (boolean): be verbose
        encoding (optional, str): encoding to pass to open()
            defaults to "utf-8"
        kwargs (optional): kwargs for son.serialize.load

    Returns:
        metadata, data: content of file (None, [] if empty)
    """

    metadata, reader = _open(file, verbose=verbose, encoding=encoding, **kwargs)
    data = list(reader)

    return metadata, data


def load_last(file, verbose=False, encoding="utf-8", **kwargs):
    """load and decode son last entry of son file

    Args:
        file (path/str): load file
        verbose (boolean): be verbose
        encoding (optional, str): encoding to pass to open()
            defaults to "utf-8"
        kwargs (optional): kwargs for son.serialize.load

    Returns:
        metadata, last: metadata and last entry of file
            (None, None) if empty
    """

    from .last import last

    if verbose:
        print(f"[son] get last entry from:  {file}", flush=True)

    metadata = get_metadata(file, encoding=encoding, **kwargs)

    with open(file, encoding=encoding) as f:
        record = last(f)
        record = serialize.load(record, **kwargs)

    return metadata, record


def _open(file, verbose=False, encoding="utf-8", **kwargs):
    """open and decode son file on the fly

    Return metadata and an iterator that parses a son file one entry at a time.

    Since this method does not load the file into memory all at once,
    it should be used for performance-sensitive applications with large files.

    Metadata entries that are not the first entry of the file are ignored.

    Args:
        file (path/str): load file
        verbose (boolean): be verbose
        encoding (optional, str): encoding to pass to open()
            defaults to "utf-8"
        kwargs (optional): kwargs for son.serialize.load

    Returns:
        (metadata, reader): metadata is either an object or None,
            reader is a generator iterator yielding de-serialized
            objects from the son file

    """
    if verbose:
        print(f"[son] open file:  {file}", flush=True)

    metadata = get_metadata(file, encoding=encoding, **kwargs)

    return metadata, reader(file, encoding=encoding, **kwargs)


def get_metadata(file, encoding="utf-8", **kwargs):
    metadata = None

    with open(file, encoding=encoding) as f:
        try:
            record, is_metadata = next(stream.read(f))
            if is_metadata:
                metadata = serialize.load(record, **kwargs)
        except StopIteration:
            pass  # file is empty

    return metadata


def reader(file, encoding="utf-8", **kwargs):
    with open(file, encoding=encoding) as f:
        for record, is_metadata in stream.read(f):
            if not is_metadata:  # silently skip metadata
                obj = serialize.load(record, **kwargs)
                yield obj
