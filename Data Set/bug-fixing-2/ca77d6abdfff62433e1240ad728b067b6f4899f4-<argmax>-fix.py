

def argmax(self, axis=None, out=None):
    'Return indices of maximum elements along an axis.\n\n        Implicit zero elements are also taken into account. If there are\n        several maximum values, the index of the first occurrence is returned.\n\n        Parameters\n        ----------\n        axis : {-2, -1, 0, 1, None}, optional\n            Axis along which the argmax is computed. If None (default), index\n            of the maximum element in the flatten data is returned.\n        out : None, optional\n            This argument is in the signature *solely* for NumPy\n            compatibility reasons. Do not pass in anything except for\n            the default value, as this argument is not used.\n\n        Returns\n        -------\n        ind : np.matrix or int\n            Indices of maximum elements. If matrix, its size along `axis` is 1.\n        '
    return self._arg_min_or_max(axis, out, np.argmax, np.greater)
