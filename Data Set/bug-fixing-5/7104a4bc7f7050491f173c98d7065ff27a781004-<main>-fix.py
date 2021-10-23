def main():
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    e = ((((a * b) * b) + (((2 * b) * a) * b)) ** c)
    print('')
    pprint(e)
    print('')