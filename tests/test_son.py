"""creates a file test.son and reads back in"""

import son
from pathlib import Path

fname = "test.son"

# metadata
m = {"purpose": "store biography data", "version": 0.1}

# data points
d1 = {"first name": "Hildegard", "second name": "Kneef", "age": 93}
d2 = {"first name": "Wiglaf", "second name": "Droste", "age": 57}


def write(file, metadata, data, clean_first=True):
    if Path(file).exists() and clean_first:
        Path(file).unlink()

    if metadata is not None:
        son.dump(metadata, file, is_metadata=True, indent=2)

    for obj in data:
        son.dump(obj, file, indent=2)


def test_write(fname=fname, metadata=m, data=[d1, d2], clean_first=True):
    """test son.dump"""

    write(fname, m, data, clean_first=clean_first)


def test_read(fname=fname, m=m, d=[d1, d2]):
    """test son.load and son.open"""
    metadata, data = son.load(fname)

    assert metadata == m
    assert data == d

    metadata, reader = son.open(fname)

    assert metadata == m

    for i, data in enumerate(reader):
        assert data == d[i]


def test_write_again(fname=fname):
    """test if writing again throws error"""

    try:
        test_write(clean_first=False)
        raise RuntimeError("FIXME")
    except FileExistsError:
        pass


def test_write_no_metadata(fname=fname, data=[d1, d2]):
    """test son.dump w/o metadata"""

    write(fname, None, data, clean_first=True)


def test_read_no_metadata(fname=fname):
    """test son.load w/o metadata"""
    metadata, data = son.load(fname)

    assert metadata is None
    assert data == [d1, d2]


if __name__ == "__main__":
    test_write()
    test_read()
    test_write_again()
    test_write_no_metadata()
    test_read_no_metadata()
