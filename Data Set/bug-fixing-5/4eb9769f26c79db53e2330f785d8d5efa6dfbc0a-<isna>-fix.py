def isna(self):
    '\n        Detect missing values\n\n        Missing values (-1 in .codes) are detected.\n\n        Returns\n        -------\n        a boolean array of whether my values are null\n\n        See also\n        --------\n        isna : top-level isna\n        isnull : alias of isna\n        Categorical.notna : boolean inverse of Categorical.isna\n\n        '
    ret = (self._codes == (- 1))
    return ret