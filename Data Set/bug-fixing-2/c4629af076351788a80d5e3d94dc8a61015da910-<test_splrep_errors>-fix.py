

def test_splrep_errors(self):
    (x, y) = (self.xx, self.yy)
    y2 = np.c_[(y, y)]
    with assert_raises(ValueError):
        splrep(x, y2)
    with assert_raises(ValueError):
        _impl.splrep(x, y2)
    with assert_raises(TypeError, match='m > k must hold'):
        splrep(x[:3], y[:3])
    with assert_raises(TypeError, match='m > k must hold'):
        _impl.splrep(x[:3], y[:3])
