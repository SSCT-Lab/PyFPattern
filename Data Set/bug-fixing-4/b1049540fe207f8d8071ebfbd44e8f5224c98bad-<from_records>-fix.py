@classmethod
def from_records(cls, data, index=None, exclude=None, columns=None, coerce_float=False, nrows=None):
    '\n        Convert structured or record ndarray to DataFrame.\n\n        Parameters\n        ----------\n        data : ndarray (structured dtype), list of tuples, dict, or DataFrame\n        index : str, list of fields, array-like\n            Field of array to use as the index, alternately a specific set of\n            input labels to use.\n        exclude : sequence, default None\n            Columns or fields to exclude.\n        columns : sequence, default None\n            Column names to use. If the passed data do not have names\n            associated with them, this argument provides names for the\n            columns. Otherwise this argument indicates the order of the columns\n            in the result (any names not found in the data will become all-NA\n            columns).\n        coerce_float : bool, default False\n            Attempt to convert values of non-string, non-numeric objects (like\n            decimal.Decimal) to floating point, useful for SQL result sets.\n        nrows : int, default None\n            Number of rows to read if data is an iterator.\n\n        Returns\n        -------\n        DataFrame\n        '
    if (columns is not None):
        columns = ensure_index(columns)
    if is_iterator(data):
        if (nrows == 0):
            return cls()
        try:
            first_row = next(data)
        except StopIteration:
            return cls(index=index, columns=columns)
        dtype = None
        if (hasattr(first_row, 'dtype') and first_row.dtype.names):
            dtype = first_row.dtype
        values = [first_row]
        if (nrows is None):
            values += data
        else:
            values.extend(itertools.islice(data, (nrows - 1)))
        if (dtype is not None):
            data = np.array(values, dtype=dtype)
        else:
            data = values
    if isinstance(data, dict):
        if (columns is None):
            columns = arr_columns = ensure_index(sorted(data))
            arrays = [data[k] for k in columns]
        else:
            arrays = []
            arr_columns = []
            for (k, v) in data.items():
                if (k in columns):
                    arr_columns.append(k)
                    arrays.append(v)
            (arrays, arr_columns) = reorder_arrays(arrays, arr_columns, columns)
    elif isinstance(data, (np.ndarray, DataFrame)):
        (arrays, columns) = to_arrays(data, columns)
        if (columns is not None):
            columns = ensure_index(columns)
        arr_columns = columns
    else:
        (arrays, arr_columns) = to_arrays(data, columns, coerce_float=coerce_float)
        arr_columns = ensure_index(arr_columns)
        if (columns is not None):
            columns = ensure_index(columns)
        else:
            columns = arr_columns
    if (exclude is None):
        exclude = set()
    else:
        exclude = set(exclude)
    result_index = None
    if (index is not None):
        if (isinstance(index, str) or (not hasattr(index, '__iter__'))):
            i = columns.get_loc(index)
            exclude.add(index)
            if (len(arrays) > 0):
                result_index = Index(arrays[i], name=index)
            else:
                result_index = Index([], name=index)
        else:
            try:
                index_data = [arrays[arr_columns.get_loc(field)] for field in index]
                result_index = ensure_index_from_sequences(index_data, names=index)
                exclude.update(index)
            except Exception:
                result_index = index
    if any(exclude):
        arr_exclude = [x for x in exclude if (x in arr_columns)]
        to_remove = [arr_columns.get_loc(col) for col in arr_exclude]
        arrays = [v for (i, v) in enumerate(arrays) if (i not in to_remove)]
        arr_columns = arr_columns.drop(arr_exclude)
        columns = columns.drop(exclude)
    mgr = arrays_to_mgr(arrays, arr_columns, result_index, columns)
    return cls(mgr)