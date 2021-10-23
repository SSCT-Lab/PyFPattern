def __init__(self, interval, stat_func=None, pattern='.*', sort=False):
    if (stat_func is None):

        def asum_stat(x):
            'returns |x|/size(x), async execution.'
            return (ndarray.norm(x) / sqrt(x.size))
        stat_func = asum_stat
    self.stat_func = stat_func
    self.interval = interval
    self.activated = False
    self.queue = []
    self.step = 0
    self.exes = []
    self.re_prog = re.compile(pattern)
    self.sort = sort

    def stat_helper(name, array):
        'wrapper for executor callback'
        if ((not self.activated) or (not self.re_prog.match(py_str(name)))):
            return
        array = ctypes.cast(array, NDArrayHandle)
        array = NDArray(array, writable=False)
        self.queue.append((self.step, py_str(name), self.stat_func(array)))
    self.stat_helper = stat_helper