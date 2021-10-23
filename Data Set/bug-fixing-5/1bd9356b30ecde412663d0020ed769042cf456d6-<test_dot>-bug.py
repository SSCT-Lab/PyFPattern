@with_seed(0)
def test_dot():
    nrepeat = 10
    maxdim = 4
    for repeat in range(nrepeat):
        s = tuple(np.random.randint(1, 500, size=3))
        check_bind_with_uniform((lambda x, y: np.dot(x, y)), (lambda g, x, y: (np.dot(g, y.T), np.dot(x.T, g))), 2, lshape=(s[0], s[1]), rshape=(s[1], s[2]), sf=mx.symbol.dot)
    for repeat in range(nrepeat):
        s = tuple(np.random.randint(1, 500, size=1))
        check_bind_with_uniform((lambda x, y: np.dot(x, y)), (lambda g, x, y: ((g * y), (g * x))), 2, lshape=(s[0],), rshape=(s[0],), sf=mx.symbol.dot)