def isna(self):
    '\n        Detect missing values\n\n        Both missing values (-1 in .codes) and NA as a category are detected.\n\n        Returns\n        -------\n        a boolean array of whether my values are null\n\n        See also\n        --------\n        isna : top-level isna\n        isnull : alias of isna\n        Categorical.notna : boolean inverse of Categorical.isna\n\n        '
    ret = (self._codes == (- 1))
    if (self.categories.dtype.kind in ['S', 'O', 'f']):
        if (np.nan in self.categories):
            nan_pos = np.where(isna(self.categories))[0]
            ret = np.logical_or(ret, (self._codes == nan_pos))
    return ret