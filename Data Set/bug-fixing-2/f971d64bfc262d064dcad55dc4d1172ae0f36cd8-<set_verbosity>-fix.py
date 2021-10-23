

def set_verbosity(self, verbose=False, print_func=None):
    'Switch on/off verbose mode\n\n        Parameters\n        ----------\n        verbose : bool\n            switch on/off verbose mode\n        print_func : function\n            A function that computes statistics of initialized arrays.\n            Takes an `NDArray` and returns an `str`. Defaults to mean\n            absolute value str((abs(x)/size(x)).asscalar()).\n        '
    self._verbose = verbose
    if (print_func is None):

        def asum_stat(x):
            'returns |x|/size(x), async execution.'
            return str((ndarray.norm(x) / sqrt(x.size)).asscalar())
        print_func = asum_stat
    self._print_func = print_func
    return self
