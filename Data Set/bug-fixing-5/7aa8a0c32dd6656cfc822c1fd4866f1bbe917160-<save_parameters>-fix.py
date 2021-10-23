def save_parameters(self, filename):
    'Save parameters to file.\n\n        Saved parameters can only be loaded with `load_parameters`. Note that this\n        method only saves parameters, not model structure. If you want to save\n        model structures, please use :py:meth:`HybridBlock.export`.\n\n        Parameters\n        ----------\n        filename : str\n            Path to file.\n\n        References\n        ----------\n        `Saving and Loading Gluon Models\n\n        <https://mxnet.incubator.apache.org/tutorials/gluon/save_load_params.html>`_\n        '
    params = self._collect_params_with_prefix()
    arg_dict = {key: val._reduce() for (key, val) in params.items()}
    ndarray.save(filename, arg_dict)