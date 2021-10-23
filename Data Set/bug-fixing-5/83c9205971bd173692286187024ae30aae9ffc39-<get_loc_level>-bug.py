def get_loc_level(self, key, level=0, drop_level=True):
    '\n        Get integer location slice for requested label or tuple\n\n        Parameters\n        ----------\n        key : label or tuple\n        level : int/level name or list thereof\n\n        Returns\n        -------\n        loc : int or slice object\n        '

    def maybe_droplevels(indexer, levels, drop_level):
        if (not drop_level):
            return self[indexer]
        orig_index = new_index = self[indexer]
        levels = [self._get_level_number(i) for i in levels]
        for i in sorted(levels, reverse=True):
            try:
                new_index = new_index.droplevel(i)
            except:
                return orig_index
        return new_index
    if isinstance(level, (tuple, list)):
        if (len(key) != len(level)):
            raise AssertionError('Key for location must have same length as number of levels')
        result = None
        for (lev, k) in zip(level, key):
            (loc, new_index) = self.get_loc_level(k, level=lev)
            if isinstance(loc, slice):
                mask = np.zeros(len(self), dtype=bool)
                mask[loc] = True
                loc = mask
            result = (loc if (result is None) else (result & loc))
        return (result, maybe_droplevels(result, level, drop_level))
    level = self._get_level_number(level)
    if isinstance(key, list):
        key = tuple(key)
    if (isinstance(key, tuple) and (level == 0)):
        try:
            if (key in self.levels[0]):
                indexer = self._get_level_indexer(key, level=level)
                new_index = maybe_droplevels(indexer, [0], drop_level)
                return (indexer, new_index)
        except TypeError:
            pass
        if (not any((isinstance(k, slice) for k in key))):

            def partial_selection(key, indexer=None):
                if (indexer is None):
                    indexer = self.get_loc(key)
                ilevels = [i for i in range(len(key)) if (key[i] != slice(None, None))]
                return (indexer, maybe_droplevels(indexer, ilevels, drop_level))
            if (len(key) == self.nlevels):
                if self.is_unique:
                    all_dates = [(l.is_all_dates and (not isinstance(k, compat.string_types))) for (k, l) in zip(key, self.levels)]
                    can_index_exactly = any(all_dates)
                    if (any([l.is_all_dates for (k, l) in zip(key, self.levels)]) and (not can_index_exactly)):
                        indexer = self.get_loc(key)
                        if ((not isinstance(indexer, slice)) or ((indexer.stop - indexer.start) != 1)):
                            return partial_selection(key, indexer)
                        key = tuple(self[indexer].tolist()[0])
                    return (self._engine.get_loc(_values_from_object(key)), None)
                else:
                    return partial_selection(key)
            else:
                return partial_selection(key)
        else:
            indexer = None
            for (i, k) in enumerate(key):
                if (not isinstance(k, slice)):
                    k = self._get_level_indexer(k, level=i)
                    if isinstance(k, slice):
                        if ((k.start == 0) and (k.stop == len(self))):
                            k = slice(None, None)
                    else:
                        k_index = k
                if isinstance(k, slice):
                    if (k == slice(None, None)):
                        continue
                    else:
                        raise TypeError(key)
                if (indexer is None):
                    indexer = k_index
                else:
                    indexer &= k_index
            if (indexer is None):
                indexer = slice(None, None)
            ilevels = [i for i in range(len(key)) if (key[i] != slice(None, None))]
            return (indexer, maybe_droplevels(indexer, ilevels, drop_level))
    else:
        indexer = self._get_level_indexer(key, level=level)
        return (indexer, maybe_droplevels(indexer, [level], drop_level))