from math import ceil
try:
    from math import log2
except ImportError as e:
    from math import log

    def log2(x):
        return log(x, 2)


from uuid import UUID, uuid4


digit_chars = "bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ3456789"
chars_map = {dig: idx for idx, dig in enumerate(digit_chars)}


def uuid2str(value):
    result = []
    unevaluated = value.int
    for unused in range(int(ceil(128 / log2(len(digit_chars))))):
        unevaluated, remainder = divmod(unevaluated, len(digit_chars))
        result.append(digit_chars[remainder])
    return "".join(result)


def str2uuid(value):
    acc = 0
    mul = 1
    for digit in value:
        acc += chars_map[digit] * mul
        mul *= len(digit_chars)
    return UUID(int=acc)


def generate_scielo_pid():
    return uuid2str(uuid4())