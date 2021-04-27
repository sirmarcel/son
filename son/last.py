"""son.last

Read only the *last* entry of a son file.

"""

from .stream import token_metadata, token_record, delimiter, rebuild


def last(stream):
    # this will ONLY work with io.TextIOWrapper-derived streams,
    # such as the one obtained with open(file, encoding="utf-8"),
    # but NOT with StringIO (since it has a slightly different API)
    from lz.reversal import reverse

    record = []
    started = False
    for line in reverse(stream):
        if started:
            if line == delimiter(token_metadata) or line == delimiter(token_record):
                break
            else:
                # lines seem to include leading newlines,
                # which we strip for good measure
                record.append(line.strip() + "\n")

        else:
            if line == delimiter(token_record):
                started = True

    return rebuild(reversed(record))
