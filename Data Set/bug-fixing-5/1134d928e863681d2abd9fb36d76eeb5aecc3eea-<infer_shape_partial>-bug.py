def infer_shape_partial(self, *args, **kwargs):
    'Partially infer the shape. The same as `infer_shape`, except that the partial\n        results can be returned.\n        '
    return self._infer_shape_impl(True, *args, **kwargs)