

def replace(self, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad', axis=None):
    "\n        Replace values given in 'to_replace' with 'value'.\n\n        Parameters\n        ----------\n        to_replace : str, regex, list, dict, Series, numeric, or None\n\n            * str or regex:\n\n                - str: string exactly matching `to_replace` will be replaced\n                  with `value`\n                - regex: regexs matching `to_replace` will be replaced with\n                  `value`\n\n            * list of str, regex, or numeric:\n\n                - First, if `to_replace` and `value` are both lists, they\n                  **must** be the same length.\n                - Second, if ``regex=True`` then all of the strings in **both**\n                  lists will be interpreted as regexs otherwise they will match\n                  directly. This doesn't matter much for `value` since there\n                  are only a few possible substitution regexes you can use.\n                - str and regex rules apply as above.\n\n            * dict:\n\n                - Nested dictionaries, e.g., {'a': {'b': nan}}, are read as\n                  follows: look in column 'a' for the value 'b' and replace it\n                  with nan. You can nest regular expressions as well. Note that\n                  column names (the top-level dictionary keys in a nested\n                  dictionary) **cannot** be regular expressions.\n                - Keys map to column names and values map to substitution\n                  values. You can treat this as a special case of passing two\n                  lists except that you are specifying the column to search in.\n\n            * None:\n\n                - This means that the ``regex`` argument must be a string,\n                  compiled regular expression, or list, dict, ndarray or Series\n                  of such elements. If `value` is also ``None`` then this\n                  **must** be a nested dictionary or ``Series``.\n\n            See the examples section for examples of each of these.\n        value : scalar, dict, list, str, regex, default None\n            Value to use to fill holes (e.g. 0), alternately a dict of values\n            specifying which value to use for each column (columns not in the\n            dict will not be filled). Regular expressions, strings and lists or\n            dicts of such objects are also allowed.\n        inplace : boolean, default False\n            If True, in place. Note: this will modify any\n            other views on this object (e.g. a column from a DataFrame).\n            Returns the caller if this is True.\n        limit : int, default None\n            Maximum size gap to forward or backward fill\n        regex : bool or same types as `to_replace`, default False\n            Whether to interpret `to_replace` and/or `value` as regular\n            expressions. If this is ``True`` then `to_replace` *must* be a\n            string. Otherwise, `to_replace` must be ``None`` because this\n            parameter will be interpreted as a regular expression or a list,\n            dict, or array of regular expressions.\n        method : string, optional, {'pad', 'ffill', 'bfill'}\n            The method to use when for replacement, when ``to_replace`` is a\n            ``list``.\n\n        See Also\n        --------\n        NDFrame.reindex\n        NDFrame.asfreq\n        NDFrame.fillna\n\n        Returns\n        -------\n        filled : NDFrame\n\n        Raises\n        ------\n        AssertionError\n            * If `regex` is not a ``bool`` and `to_replace` is not ``None``.\n        TypeError\n            * If `to_replace` is a ``dict`` and `value` is not a ``list``,\n              ``dict``, ``ndarray``, or ``Series``\n            * If `to_replace` is ``None`` and `regex` is not compilable into a\n              regular expression or is a list, dict, ndarray, or Series.\n        ValueError\n            * If `to_replace` and `value` are ``list`` s or ``ndarray`` s, but\n              they are not the same length.\n\n        Notes\n        -----\n        * Regex substitution is performed under the hood with ``re.sub``. The\n          rules for substitution for ``re.sub`` are the same.\n        * Regular expressions will only substitute on strings, meaning you\n          cannot provide, for example, a regular expression matching floating\n          point numbers and expect the columns in your frame that have a\n          numeric dtype to be matched. However, if those floating point numbers\n          *are* strings, then you can do this.\n        * This method has *a lot* of options. You are encouraged to experiment\n          and play with this method to gain intuition about how it works.\n\n        "
    inplace = validate_bool_kwarg(inplace, 'inplace')
    if ((not is_bool(regex)) and (to_replace is not None)):
        raise AssertionError("'to_replace' must be 'None' if 'regex' is not a bool")
    if (axis is not None):
        warnings.warn('the "axis" argument is deprecated and will be removed inv0.13; this argument has no effect')
    self._consolidate_inplace()
    if (value is None):
        if ((not is_dict_like(to_replace)) and (not is_dict_like(regex))):
            to_replace = [to_replace]
        if isinstance(to_replace, (tuple, list)):
            return _single_replace(self, to_replace, method, inplace, limit)
        if (not is_dict_like(to_replace)):
            if (not is_dict_like(regex)):
                raise TypeError('If "to_replace" and "value" are both None and "to_replace" is not a list, then regex must be a mapping')
            to_replace = regex
            regex = True
        items = list(compat.iteritems(to_replace))
        (keys, values) = (lzip(*items) or ([], []))
        are_mappings = [is_dict_like(v) for v in values]
        if any(are_mappings):
            if (not all(are_mappings)):
                raise TypeError('If a nested mapping is passed, all values of the top level mapping must be mappings')
            to_rep_dict = {
                
            }
            value_dict = {
                
            }
            for (k, v) in items:
                (keys, values) = (lzip(*v.items()) or ([], []))
                if (set(keys) & set(values)):
                    raise ValueError('Replacement not allowed with overlapping keys and values')
                to_rep_dict[k] = list(keys)
                value_dict[k] = list(values)
            (to_replace, value) = (to_rep_dict, value_dict)
        else:
            (to_replace, value) = (keys, values)
        return self.replace(to_replace, value, inplace=inplace, limit=limit, regex=regex)
    else:
        for a in self._AXIS_ORDERS:
            if (not len(self._get_axis(a))):
                return self
        new_data = self._data
        if is_dict_like(to_replace):
            if is_dict_like(value):
                res = (self if inplace else self.copy())
                for (c, src) in compat.iteritems(to_replace):
                    if ((c in value) and (c in self)):
                        res[c] = res[c].replace(to_replace=src, value=value[c], inplace=False, regex=regex)
                return (None if inplace else res)
            elif (not is_list_like(value)):
                keys = [(k, src) for (k, src) in compat.iteritems(to_replace) if (k in self)]
                keys_len = (len(keys) - 1)
                for (i, (k, src)) in enumerate(keys):
                    convert = (i == keys_len)
                    new_data = new_data.replace(to_replace=src, value=value, filter=[k], inplace=inplace, regex=regex, convert=convert)
            else:
                raise TypeError('value argument must be scalar, dict, or Series')
        elif is_list_like(to_replace):
            if is_list_like(value):
                if (len(to_replace) != len(value)):
                    raise ValueError(('Replacement lists must match in length. Expecting %d got %d ' % (len(to_replace), len(value))))
                new_data = self._data.replace_list(src_list=to_replace, dest_list=value, inplace=inplace, regex=regex)
            else:
                new_data = self._data.replace(to_replace=to_replace, value=value, inplace=inplace, regex=regex)
        elif (to_replace is None):
            if (not (is_re_compilable(regex) or is_list_like(regex) or is_dict_like(regex))):
                raise TypeError("'regex' must be a string or a compiled regular expression or a list or dict of strings or regular expressions, you passed a {0!r}".format(type(regex).__name__))
            return self.replace(regex, value, inplace=inplace, limit=limit, regex=True)
        elif is_dict_like(value):
            new_data = self._data
            for (k, v) in compat.iteritems(value):
                if (k in self):
                    new_data = new_data.replace(to_replace=to_replace, value=v, filter=[k], inplace=inplace, regex=regex)
        elif (not is_list_like(value)):
            new_data = self._data.replace(to_replace=to_replace, value=value, inplace=inplace, regex=regex)
        else:
            msg = 'Invalid "to_replace" type: {0!r}'.format(type(to_replace).__name__)
            raise TypeError(msg)
    if inplace:
        self._update_inplace(new_data)
    else:
        return self._constructor(new_data).__finalize__(self)
