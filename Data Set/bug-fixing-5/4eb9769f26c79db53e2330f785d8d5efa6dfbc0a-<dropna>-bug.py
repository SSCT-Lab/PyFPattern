def dropna(self):
    '\n        Return the Categorical without null values.\n\n        Both missing values (-1 in .codes) and NA as a category are detected.\n        NA is removed from the categories if present.\n\n        Returns\n        -------\n        valid : Categorical\n        '
    result = self[self.notna()]
    if isna(result.categories).any():
        result = result.remove_categories([np.nan])
    return result