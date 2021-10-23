def load_parameters(self, filename, ctx=None, allow_missing=False, ignore_extra=False):
    'Load parameters from file.\n        This function is to be used to load parameters of a Gluon model that were\n        saved using the `.save_parameters()` function. Any other use is undefined behaviour.\n        Refer to this tutorial for a complete overview of saving/loading models with\n        MXNet: https://mxnet.incubator.apache.org/tutorials/gluon/save_load_params.html\n\n        Parameters\n        ----------\n        filename : str\n            Path to parameter file.\n        ctx : Context or list of Context, default cpu()\n            Context(s) to initialize loaded parameters on.\n        allow_missing : bool, default False\n            Whether to silently skip loading parameters not represents in the file.\n        ignore_extra : bool, default False\n            Whether to silently ignore parameters from the file that are not\n            present in this Block.\n        '
    loaded = ndarray.load(filename)
    params = self._collect_params_with_prefix()
    if ((not loaded) and (not params)):
        return
    if (not any((('.' in i) for i in loaded.keys()))):
        del loaded
        self.collect_params().load(filename, ctx, allow_missing, ignore_extra, self.prefix)
        return
    if (not allow_missing):
        for name in params.keys():
            assert (name in loaded), ("Parameter '%s' is missing in file '%s', which contains parameters: %s. Set allow_missing=True to ignore missing parameters." % (name, filename, _brief_print_list(loaded.keys())))
    for name in loaded:
        if ((not ignore_extra) and (name not in params)):
            raise ValueError(("Parameter '%s' loaded from file '%s' is not present in ParameterDict, which contains parameters %s. Set ignore_extra=True to ignore. " % (name, filename, _brief_print_list(self._params.keys()))))
        if (name in params):
            params[name]._load_init(loaded[name], ctx)