@property
def strides(self):
    ' return the strides of the underlying data '
    warnings.warn('{obj}.strudes is deprecated and will be removed in a future version'.format(obj=type(self).__name__), FutureWarning, stacklevel=2)
    return self._ndarray_values.strides