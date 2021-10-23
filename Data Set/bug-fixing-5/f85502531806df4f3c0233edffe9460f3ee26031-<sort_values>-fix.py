def sort_values(self, return_indexer=False, ascending=True):
    '\n        Return sorted copy of Index.\n        '
    if return_indexer:
        _as = self.argsort()
        if (not ascending):
            _as = _as[::(- 1)]
        sorted_index = self.take(_as)
        return (sorted_index, _as)
    else:
        sorted_values = np.sort(self.asi8)
        attribs = self._get_attributes_dict()
        freq = attribs['freq']
        if ((freq is not None) and (not is_period_dtype(self))):
            if ((freq.n > 0) and (not ascending)):
                freq = (freq * (- 1))
            elif ((freq.n < 0) and ascending):
                freq = (freq * (- 1))
        attribs['freq'] = freq
        if (not ascending):
            sorted_values = sorted_values[::(- 1)]
        return self._simple_new(sorted_values, **attribs)