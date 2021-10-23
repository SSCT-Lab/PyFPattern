def save(self, filename, strip_prefix=''):
    "Save parameters to file.\n\n        Parameters\n        ----------\n        filename : str\n            Path to parameter file.\n        strip_prefix : str, default ''\n            Strip prefix from parameter names before saving.\n        "
    arg_dict = {
        
    }
    for param in self.values():
        weight = param._reduce()
        if (not param.name.startswith(strip_prefix)):
            raise ValueError(("Prefix '%s' is to be striped before saving, but Parameter's name '%s' does not start with '%s'. this may be due to your Block shares parameters from other Blocks or you forgot to use 'with name_scope()' when creating child blocks. For more info on naming, please see https://mxnet.io/api/python/docs/tutorials/packages/gluon/blocks/naming.html" % (strip_prefix, param.name, strip_prefix)))
        arg_dict[param.name[len(strip_prefix):]] = weight
    ndarray.save(filename, arg_dict)