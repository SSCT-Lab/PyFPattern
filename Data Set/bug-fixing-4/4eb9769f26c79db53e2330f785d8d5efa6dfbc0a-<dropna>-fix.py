def dropna(self):
    '\n        Return the Categorical without null values.\n\n        Missing values (-1 in .codes) are detected.\n\n        Returns\n        -------\n        valid : Categorical\n        '
    result = self[self.notna()]
    return result