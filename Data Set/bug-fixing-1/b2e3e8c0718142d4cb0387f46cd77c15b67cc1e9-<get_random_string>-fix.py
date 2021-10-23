

def get_random_string(length=8, choices=(string.ascii_letters + string.digits)):
    '\n    Generate random string\n    '
    return ''.join([choice(choices) for _ in range(length)])
