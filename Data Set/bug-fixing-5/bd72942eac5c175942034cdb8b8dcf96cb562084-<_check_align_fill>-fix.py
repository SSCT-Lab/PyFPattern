def _check_align_fill(self, frame, kind, meth, ax, fax):
    left = frame.iloc[0:4, :10]
    right = frame.iloc[2:, 6:]
    empty = frame.iloc[:0, :0]
    self._check_align(left, right, axis=ax, fill_axis=fax, how=kind, method=meth)
    self._check_align(left, right, axis=ax, fill_axis=fax, how=kind, method=meth, limit=1)
    self._check_align(empty, right, axis=ax, fill_axis=fax, how=kind, method=meth)
    self._check_align(empty, right, axis=ax, fill_axis=fax, how=kind, method=meth, limit=1)
    self._check_align(left, empty, axis=ax, fill_axis=fax, how=kind, method=meth)
    self._check_align(left, empty, axis=ax, fill_axis=fax, how=kind, method=meth, limit=1)
    self._check_align(empty, empty, axis=ax, fill_axis=fax, how=kind, method=meth)
    self._check_align(empty, empty, axis=ax, fill_axis=fax, how=kind, method=meth, limit=1)