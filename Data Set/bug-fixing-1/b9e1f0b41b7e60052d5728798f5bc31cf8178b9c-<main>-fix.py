

def main():
    x = Symbol('x')
    e = (1 / cos(x))
    print('')
    print('Series for sec(x):')
    print('')
    pprint(e.series(x, 0, 10))
    print('\n')
    e = (1 / sin(x))
    print('Series for csc(x):')
    print('')
    pprint(e.series(x, 0, 4))
    print('')
