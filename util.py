import random
import sys

def get_random(chars, size):
        return ''.join(random.choice(chars) for _ in range(size))

def get_random_nums(size=5):
    num = get_random([chr(i) for i in range(48,58)], size)
    return num

def get_random_caps(size=5):
    caps = get_random([chr(i) for i in range(65,91)], size)
    return caps

def get_random_characters(size=5):
    num = get_random([chr(i) for i in range(48,58)], size)
    small = get_random([chr(i) for i in range(97,123)], size)
    caps = get_random([chr(i) for i in range(65,91)], size)
    specials = get_random([chr(i) for i in [33,35,36,37,38,42,59,61,63] + list(range(43,47))], size)
    return random.choice([num, small, caps, specials])

def set_specific_values(tag):
    if tag == 'Applicant_ID':
        value = 'A' + get_random_nums() + '-' + get_random_caps()
    elif tag == 'Address_Line_Data':
        value = get_random_characters()

    elif tag == 'Address_Line_Data':
        value = get_random_characters()
    else:
        value = get_random_characters()
    return value