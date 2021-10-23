def read():
    'Return the contents of the Windows Common Setup as a string'
    setup_in = open(PATH)
    try:
        return setup_in.read()
    finally:
        setup_in.close()