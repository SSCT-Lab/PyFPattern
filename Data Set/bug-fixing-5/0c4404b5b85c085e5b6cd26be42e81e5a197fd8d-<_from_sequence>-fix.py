@classmethod
def _from_sequence(cls, scalars, dtype=None, copy=False):
    '\n        Construct a new ExtensionArray from a sequence of scalars.\n\n        Parameters\n        ----------\n        scalars : Sequence\n            Each element will be an instance of the scalar type for this\n            array, ``cls.dtype.type``.\n        dtype : dtype, optional\n            Construct for this particular dtype. This should be a Dtype\n            compatible with the ExtensionArray.\n        copy : bool, default False\n            If True, copy the underlying data.\n\n        Returns\n        -------\n        ExtensionArray\n        '
    raise AbstractMethodError(cls)