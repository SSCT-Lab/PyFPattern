def _set_attr(self, **kwargs):
    'Sets an attribute of the symbol.\n\n        For example. A._set_attr(foo="bar") adds the mapping ``"{foo: bar}"``\n        to the symbol\'s attribute dictionary.\n\n        Parameters\n        ----------\n        **kwargs\n            The attributes to set\n        '
    for (key, value) in kwargs.items():
        if (not isinstance(value, string_types)):
            raise ValueError('Set Attr only accepts string values')
        check_call(_LIB.MXSymbolSetAttr(self.handle, c_str(key), c_str(str(value))))