import random


def create_ref():
    ref_chars = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    )
    ref_length = 8
    count = len(ref_chars) - 1
    ref = ''
    for i in range(0, ref_length):
        ref += ref_chars[random.randint(0, count)]

    return ref
