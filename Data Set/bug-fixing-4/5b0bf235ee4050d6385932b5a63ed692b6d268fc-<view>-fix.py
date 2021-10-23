def view(self, dtype=None) -> Union[(ABCExtensionArray, np.ndarray)]:
    '\n        Return a view on the array.\n\n        Parameters\n        ----------\n        dtype : str, np.dtype, or ExtensionDtype, optional\n            Default None.\n\n        Returns\n        -------\n        ExtensionArray\n            A view of the :class:`ExtensionArray`.\n        '
    if (dtype is not None):
        raise NotImplementedError(dtype)
    return self[:]