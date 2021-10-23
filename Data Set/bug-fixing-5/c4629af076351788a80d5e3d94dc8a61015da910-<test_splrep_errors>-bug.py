def test_splrep_errors(self):
    (x, y) = (self.xx, self.yy)
    y2 = np.c_[(y, y)]
    msg = "failed in converting 3rd argument `y' of dfitpack.curfit to C/Fortran array"
    with assert_raises(Exception, message=msg):
        splrep(x, y2)
    with assert_raises(Exception, message=msg):
        _impl.splrep(x, y2)
    with assert_raises(TypeError, match='m > k must hold'):
        splrep(x[:3], y[:3])
    with assert_raises(TypeError, match='m > k must hold'):
        _impl.splrep(x[:3], y[:3])