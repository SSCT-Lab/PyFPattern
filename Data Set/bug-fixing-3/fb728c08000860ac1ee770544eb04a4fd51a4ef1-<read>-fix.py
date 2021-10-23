def read():
    'Return the contents of the Windows Common Setup as a string'
    with open(PATH) as setup_in:
        return setup_in.read()