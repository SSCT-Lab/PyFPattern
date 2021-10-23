def save_params(self, filename):
    '[Deprecated] Please use save_parameters.\n\n        Save parameters to file.\n\n        filename : str\n            Path to file.\n        '
    warnings.warn('save_params is deprecated. Please use save_parameters.')
    try:
        self.collect_params().save(filename, strip_prefix=self.prefix)
    except ValueError as e:
        raise ValueError(('%s\nsave_params is deprecated. Using save_parameters may resolve this error.' % e.message))