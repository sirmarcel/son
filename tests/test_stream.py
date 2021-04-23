import son.stream as stream

characters = "ABCDE"


def to_string(tuple_iterator):
    for t in tuple_iterator:
        yield "".join(t)


def test_roundtrip(characters=characters):
    from io import StringIO
    from itertools import permutations

    mystream = StringIO()
    stream.write(mystream, "META", is_metadata=True)
    for string in to_string(permutations(characters, 3)):
        stream.write(mystream, string, is_metadata=False)

    # new stream to read
    mystream = StringIO(mystream.getvalue())

    reader = stream.read(mystream)

    entry, is_metadata = next(reader)
    assert entry == "META\n"
    assert is_metadata is True

    for result, reference in zip(reader, to_string(permutations(characters, 3))):
        entry, is_metadata = result
        assert entry == reference + "\n"
        assert is_metadata is False


if __name__ == "__main__":
    test_roundtrip()
