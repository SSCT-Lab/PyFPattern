def __eq__(self, other):
    '\n        Check whether other equals self elementwise.\n\n        '
    if (self is masked):
        return masked
    omask = getattr(other, '_mask', nomask)
    if (omask is nomask):
        check = self.filled(0).__eq__(other)
        try:
            check = check.view(type(self))
            check._mask = self._mask
        except AttributeError:
            return check
    else:
        odata = filled(other, 0)
        check = self.filled(0).__eq__(odata).view(type(self))
        if (self._mask is nomask):
            check._mask = omask
        else:
            mask = mask_or(self._mask, omask)
            if mask.dtype.names:
                if (mask.size > 1):
                    axis = 1
                else:
                    axis = None
                try:
                    mask = mask.view((bool_, len(self.dtype))).all(axis)
                except ValueError:
                    mask = np.all([[f[n].all() for n in mask.dtype.names] for f in mask], axis=axis)
            check._mask = mask
    return check