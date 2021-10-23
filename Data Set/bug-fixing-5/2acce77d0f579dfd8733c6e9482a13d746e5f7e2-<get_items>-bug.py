def get_items(self, names):
    items = Autosummary.get_items(self, names)
    items = [self._replace_pandas_items(*item) for item in items]
    return items