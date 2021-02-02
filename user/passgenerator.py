import random
import string


def generate_password(length):
    letters = string.ascii_letters
    result = ''.join(random.choice(letters) for i in range(length))

    return result
