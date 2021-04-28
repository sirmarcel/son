"""son.stream

The heart of son: Defines how entries are written into son files,
and retrieved from them.

An entry is defined as a (multi-line) string followed by a line that contains *only*
a delimiter, either === for metadata or --- for "normal" records.

"""

token_metadata = "==="
token_record = "---"


def delimiter(token, leading_newline=False):
    if leading_newline:
        lead = "\n"
    else:
        lead = ""
    return f"{lead}{token}\n"


def write(stream, entry, is_metadata=False):
    stream.write(entry)

    if is_metadata:
        stream.write(delimiter(token_metadata, leading_newline=True))
    else:
        stream.write(delimiter(token_record, leading_newline=True))


def read(stream):
    record = []
    for line in stream:
        if line == delimiter(token_metadata):
            result = rebuild(record)
            record = []
            yield result, True
        elif line == delimiter(token_record):
            result = rebuild(record)
            record = []
            yield result, False
        else:
            record.append(line)


def rebuild(record):
    return "".join(record)
