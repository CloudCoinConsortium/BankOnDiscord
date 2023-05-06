import random
import string

def generate_alphanumeric_code(length=7, separator="-", excluded_chars="0Oo1iIlL"):
    # define the list of valid characters
    valid_chars = "".join([c for c in string.ascii_uppercase + string.digits if c not in excluded_chars])

    # generate the code
    code = ""
    for i in range(length):
        if i == 3:
            code += separator
        code += random.choice(valid_chars)

    return code
