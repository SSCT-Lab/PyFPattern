def load_dict(self, param_dict, ctx=None, allow_missing=False, ignore_extra=False, restore_prefix='', filename=None, cast_dtype=False, dtype_source='current'):
    "Load parameters from dict\n\n        Parameters\n        ----------\n        param_dict : dict\n            Dictionary containing model parameters, preprended with arg: and aux: names\n        ctx : Context or list of Context\n            Context(s) initialize loaded parameters on.\n        allow_missing : bool, default False\n            Whether to silently skip loading parameters not represented in the file.\n        ignore_extra : bool, default False\n            Whether to silently ignore parameters from the file that are not\n            present in this ParameterDict.\n        restore_prefix : str, default ''\n            prepend prefix to names of stored parameters before loading\n        filename : str, default None\n        cast_dtype : bool, default False\n            Cast the data type of the NDArray loaded from the checkpoint to the dtype\n            provided by the Parameter if any\n        "
    lprefix = len(restore_prefix)
    loaded = ([((k[4:] if (k.startswith('arg:') or k.startswith('aux:')) else k), v) for (k, v) in param_dict.items()] if isinstance(param_dict, dict) else param_dict)
    arg_dict = {(restore_prefix + k): v for (k, v) in loaded}
    error_str = (('file: %s' % filename) if filename else 'param_dict')
    if (not allow_missing):
        for name in self.keys():
            assert (name in arg_dict), ("Parameter '%s' is missing in %s, which contains parameters: %s. Please make sure source and target networks have the same prefix.For more info on naming, please see https://mxnet.io/api/python/docs/tutorials/packages/gluon/blocks/naming.html" % (name[lprefix:], error_str, _brief_print_list(arg_dict.keys())))
    for name in arg_dict:
        if (name not in self._params):
            assert ignore_extra, ("Parameter '%s' loaded from %s is not present in ParameterDict, choices are: %s. Set ignore_extra to True to ignore. Please make sure source and target networks have the same prefix.For more info on naming, please see https://mxnet.io/api/python/docs/tutorials/packages/gluon/blocks/naming.html" % (name[lprefix:], error_str, _brief_print_list(self._params.keys())))
            continue
        self[name]._load_init(arg_dict[name], ctx, cast_dtype=cast_dtype, dtype_source=dtype_source)