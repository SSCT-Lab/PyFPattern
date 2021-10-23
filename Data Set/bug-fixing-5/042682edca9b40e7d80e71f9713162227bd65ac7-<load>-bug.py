def load(self, filename, ctx=None, allow_missing=False, ignore_extra=False, restore_prefix='', cast_dtype=False, dtype_source='current'):
    "Load parameters from file.\n\n        Parameters\n        ----------\n        filename : str\n            Path to parameter file.\n        ctx : Context or list of Context\n            Context(s) initialize loaded parameters on.\n        allow_missing : bool, default False\n            Whether to silently skip loading parameters not represents in the file.\n        ignore_extra : bool, default False\n            Whether to silently ignore parameters from the file that are not\n            present in this ParameterDict.\n        restore_prefix : str, default ''\n            prepend prefix to names of stored parameters before loading.\n        cast_dtype : bool, default False\n            Cast the data type of the parameter\n        dtype_source : str, default 'current'\n            must be in {'current', 'saved'}\n            Only valid if cast_dtype=True, specify the source of the dtype for casting\n            the parameters\n        "
    if restore_prefix:
        for name in self.keys():
            assert name.startswith(restore_prefix), ("restore_prefix is '%s' but Parameters name '%s' does not start with '%s'" % (restore_prefix, name, restore_prefix))
    ndarray_load = ndarray.load(filename)
    self.load_dict(ndarray_load, ctx, allow_missing, ignore_extra, restore_prefix, filename, cast_dtype, dtype_source)