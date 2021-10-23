

def remove_unused_levels(self):
    "\n        create a new MultiIndex from the current that removing\n        unused levels, meaning that they are not expressed in the labels\n\n        The resulting MultiIndex will have the same outward\n        appearance, meaning the same .values and ordering. It will also\n        be .equals() to the original.\n\n        .. versionadded:: 0.20.0\n\n        Returns\n        -------\n        MultiIndex\n\n        Examples\n        --------\n        >>> i = pd.MultiIndex.from_product([range(2), list('ab')])\n        MultiIndex(levels=[[0, 1], ['a', 'b']],\n                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]])\n\n\n        >>> i[2:]\n        MultiIndex(levels=[[0, 1], ['a', 'b']],\n                   labels=[[1, 1], [0, 1]])\n\n        The 0 from the first level is not represented\n        and can be removed\n\n        >>> i[2:].remove_unused_levels()\n        MultiIndex(levels=[[1], ['a', 'b']],\n                   labels=[[0, 0], [0, 1]])\n\n        "
    new_levels = []
    new_labels = []
    changed = False
    for (lev, lab) in zip(self.levels, self.labels):
        uniques = algos.unique(lab)
        na_idx = np.where((uniques == (- 1)))[0]
        if (len(uniques) != (len(lev) + len(na_idx))):
            changed = True
            if len(na_idx):
                uniques[[0, na_idx[0]]] = uniques[[na_idx[0], 0]]
            label_mapping = np.zeros((len(lev) + len(na_idx)))
            label_mapping[uniques] = (np.arange(len(uniques)) - len(na_idx))
            lab = label_mapping[lab]
            lev = lev.take(uniques[len(na_idx):])
        new_levels.append(lev)
        new_labels.append(lab)
    result = self._shallow_copy()
    if changed:
        result._reset_identity()
        result._set_levels(new_levels, validate=False)
        result._set_labels(new_labels, validate=False)
    return result
