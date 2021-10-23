def view(self, dtype=None, type=None, fill_value=None):
    "\n        Return a view of the MaskedArray data\n\n        Parameters\n        ----------\n        dtype : data-type or ndarray sub-class, optional\n            Data-type descriptor of the returned view, e.g., float32 or int16.\n            The default, None, results in the view having the same data-type\n            as `a`. As with ``ndarray.view``, dtype can also be specified as\n            an ndarray sub-class, which then specifies the type of the\n            returned object (this is equivalent to setting the ``type``\n            parameter).\n        type : Python type, optional\n            Type of the returned view, e.g., ndarray or matrix.  Again, the\n            default None results in type preservation.\n\n        Notes\n        -----\n\n        ``a.view()`` is used two different ways:\n\n        ``a.view(some_dtype)`` or ``a.view(dtype=some_dtype)`` constructs a view\n        of the array's memory with a different data-type.  This can cause a\n        reinterpretation of the bytes of memory.\n\n        ``a.view(ndarray_subclass)`` or ``a.view(type=ndarray_subclass)`` just\n        returns an instance of `ndarray_subclass` that looks at the same array\n        (same shape, dtype, etc.)  This does not cause a reinterpretation of the\n        memory.\n\n        If `fill_value` is not specified, but `dtype` is specified (and is not\n        an ndarray sub-class), the `fill_value` of the MaskedArray will be\n        reset. If neither `fill_value` nor `dtype` are specified (or if\n        `dtype` is an ndarray sub-class), then the fill value is preserved.\n        Finally, if `fill_value` is specified, but `dtype` is not, the fill\n        value is set to the specified value.\n\n        For ``a.view(some_dtype)``, if ``some_dtype`` has a different number of\n        bytes per entry than the previous dtype (for example, converting a\n        regular array to a structured array), then the behavior of the view\n        cannot be predicted just from the superficial appearance of ``a`` (shown\n        by ``print(a)``). It also depends on exactly how ``a`` is stored in\n        memory. Therefore if ``a`` is C-ordered versus fortran-ordered, versus\n        defined as a slice or transpose, etc., the view may give different\n        results.\n        "
    if (dtype is None):
        if (type is None):
            output = ndarray.view(self)
        else:
            output = ndarray.view(self, type)
    elif (type is None):
        try:
            if issubclass(dtype, ndarray):
                output = ndarray.view(self, dtype)
                dtype = None
            else:
                output = ndarray.view(self, dtype)
        except TypeError:
            output = ndarray.view(self, dtype)
    else:
        output = ndarray.view(self, dtype, type)
    if (getattr(output, '_mask', nomask) is not nomask):
        output._mask = output._mask.view()
    if (getattr(output, '_fill_value', None) is not None):
        if (fill_value is None):
            if (dtype is None):
                pass
            else:
                output._fill_value = None
        else:
            output.fill_value = fill_value
    return output