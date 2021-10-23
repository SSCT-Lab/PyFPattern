def loadtxt(fname, dtype=float, comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0):
    '\n    Load data from a text file.\n\n    Each row in the text file must have the same number of values.\n\n    Parameters\n    ----------\n    fname : file, str, or pathlib.Path\n        File, filename, or generator to read.  If the filename extension is\n        ``.gz`` or ``.bz2``, the file is first decompressed. Note that\n        generators should return byte strings for Python 3k.\n    dtype : data-type, optional\n        Data-type of the resulting array; default: float.  If this is a\n        structured data-type, the resulting array will be 1-dimensional, and\n        each row will be interpreted as an element of the array.  In this\n        case, the number of columns used must match the number of fields in\n        the data-type.\n    comments : str or sequence, optional\n        The characters or list of characters used to indicate the start of a\n        comment;\n        default: \'#\'.\n    delimiter : str, optional\n        The string used to separate values.  By default, this is any\n        whitespace.\n    converters : dict, optional\n        A dictionary mapping column number to a function that will convert\n        that column to a float.  E.g., if column 0 is a date string:\n        ``converters = {0: datestr2num}``.  Converters can also be used to\n        provide a default value for missing data (but see also `genfromtxt`):\n        ``converters = {3: lambda s: float(s.strip() or 0)}``.  Default: None.\n    skiprows : int, optional\n        Skip the first `skiprows` lines; default: 0.\n\n    usecols : int or sequence, optional\n        Which columns to read, with 0 being the first. For example,\n        usecols = (1,4,5) will extract the 2nd, 5th and 6th columns.\n        The default, None, results in all columns being read.\n\n        .. versionadded:: 1.11.0\n\n        Also when a single column has to be read it is possible to use\n        an integer instead of a tuple. E.g ``usecols = 3`` reads the\n        fourth column the same way as `usecols = (3,)`` would.\n\n    unpack : bool, optional\n        If True, the returned array is transposed, so that arguments may be\n        unpacked using ``x, y, z = loadtxt(...)``.  When used with a structured\n        data-type, arrays are returned for each field.  Default is False.\n    ndmin : int, optional\n        The returned array will have at least `ndmin` dimensions.\n        Otherwise mono-dimensional axes will be squeezed.\n        Legal values: 0 (default), 1 or 2.\n\n        .. versionadded:: 1.6.0\n\n    Returns\n    -------\n    out : ndarray\n        Data read from the text file.\n\n    See Also\n    --------\n    load, fromstring, fromregex\n    genfromtxt : Load data with missing values handled as specified.\n    scipy.io.loadmat : reads MATLAB data files\n\n    Notes\n    -----\n    This function aims to be a fast reader for simply formatted files.  The\n    `genfromtxt` function provides more sophisticated handling of, e.g.,\n    lines with missing values.\n\n    .. versionadded:: 1.10.0\n\n    The strings produced by the Python float.hex method can be used as\n    input for floats.\n\n    Examples\n    --------\n    >>> from io import StringIO   # StringIO behaves like a file object\n    >>> c = StringIO("0 1\\n2 3")\n    >>> np.loadtxt(c)\n    array([[ 0.,  1.],\n           [ 2.,  3.]])\n\n    >>> d = StringIO("M 21 72\\nF 35 58")\n    >>> np.loadtxt(d, dtype={\'names\': (\'gender\', \'age\', \'weight\'),\n    ...                      \'formats\': (\'S1\', \'i4\', \'f4\')})\n    array([(\'M\', 21, 72.0), (\'F\', 35, 58.0)],\n          dtype=[(\'gender\', \'|S1\'), (\'age\', \'<i4\'), (\'weight\', \'<f4\')])\n\n    >>> c = StringIO("1,0,2\\n3,0,4")\n    >>> x, y = np.loadtxt(c, delimiter=\',\', usecols=(0, 2), unpack=True)\n    >>> x\n    array([ 1.,  3.])\n    >>> y\n    array([ 2.,  4.])\n\n    '
    if (comments is not None):
        if isinstance(comments, (basestring, bytes)):
            comments = [asbytes(comments)]
        else:
            comments = [asbytes(comment) for comment in comments]
        comments = (re.escape(comment) for comment in comments)
        regex_comments = re.compile(asbytes('|').join(comments))
    user_converters = converters
    if (delimiter is not None):
        delimiter = asbytes(delimiter)
    if (usecols is not None):
        try:
            usecols_as_list = list(usecols)
        except TypeError:
            usecols_as_list = [usecols]
        for col_idx in usecols_as_list:
            try:
                opindex(col_idx)
            except TypeError as e:
                e.args = (('usecols must be an int or a sequence of ints but it contains at least one element of type %s' % type(col_idx)),)
                raise
        usecols = usecols_as_list
    fown = False
    try:
        if is_pathlib_path(fname):
            fname = str(fname)
        if _is_string_like(fname):
            fown = True
            if fname.endswith('.gz'):
                import gzip
                fh = iter(gzip.GzipFile(fname))
            elif fname.endswith('.bz2'):
                import bz2
                fh = iter(bz2.BZ2File(fname))
            elif (sys.version_info[0] == 2):
                fh = iter(open(fname, 'U'))
            else:
                fh = iter(open(fname))
        else:
            fh = iter(fname)
    except TypeError:
        raise ValueError('fname must be a string, file handle, or generator')
    X = []

    def flatten_dtype(dt):
        'Unpack a structured data-type, and produce re-packing info.'
        if (dt.names is None):
            shape = dt.shape
            if (len(shape) == 0):
                return ([dt.base], None)
            else:
                packing = [(shape[(- 1)], list)]
                if (len(shape) > 1):
                    for dim in dt.shape[(- 2)::(- 1)]:
                        packing = [((dim * packing[0][0]), (packing * dim))]
                return (([dt.base] * int(np.prod(dt.shape))), packing)
        else:
            types = []
            packing = []
            for field in dt.names:
                (tp, bytes) = dt.fields[field]
                (flat_dt, flat_packing) = flatten_dtype(tp)
                types.extend(flat_dt)
                if (len(tp.shape) > 0):
                    packing.extend(flat_packing)
                else:
                    packing.append((len(flat_dt), flat_packing))
            return (types, packing)

    def pack_items(items, packing):
        'Pack items into nested lists based on re-packing info.'
        if (packing is None):
            return items[0]
        elif (packing is tuple):
            return tuple(items)
        elif (packing is list):
            return list(items)
        else:
            start = 0
            ret = []
            for (length, subpacking) in packing:
                ret.append(pack_items(items[start:(start + length)], subpacking))
                start += length
            return tuple(ret)

    def split_line(line):
        'Chop off comments, strip, and split at delimiter.\n\n        Note that although the file is opened as text, this function\n        returns bytes.\n\n        '
        line = asbytes(line)
        if (comments is not None):
            line = regex_comments.split(asbytes(line), maxsplit=1)[0]
        line = line.strip(asbytes('\r\n'))
        if line:
            return line.split(delimiter)
        else:
            return []
    try:
        dtype = np.dtype(dtype)
        defconv = _getconv(dtype)
        for i in range(skiprows):
            next(fh)
        first_vals = None
        try:
            while (not first_vals):
                first_line = next(fh)
                first_vals = split_line(first_line)
        except StopIteration:
            first_line = ''
            first_vals = []
            warnings.warn(('loadtxt: Empty input file: "%s"' % fname))
        N = len((usecols or first_vals))
        (dtype_types, packing) = flatten_dtype(dtype)
        if (len(dtype_types) > 1):
            converters = [_getconv(dt) for dt in dtype_types]
        else:
            converters = [defconv for i in range(N)]
            if (N > 1):
                packing = [(N, tuple)]
        for (i, conv) in (user_converters or {
            
        }).items():
            if usecols:
                try:
                    i = usecols.index(i)
                except ValueError:
                    continue
            converters[i] = conv
        for (i, line) in enumerate(itertools.chain([first_line], fh)):
            vals = split_line(line)
            if (len(vals) == 0):
                continue
            if usecols:
                vals = [vals[i] for i in usecols]
            if (len(vals) != N):
                line_num = ((i + skiprows) + 1)
                raise ValueError(('Wrong number of columns at line %d' % line_num))
            items = [conv(val) for (conv, val) in zip(converters, vals)]
            items = pack_items(items, packing)
            X.append(items)
    finally:
        if fown:
            fh.close()
    X = np.array(X, dtype)
    if ((X.ndim == 3) and (X.shape[:2] == (1, 1))):
        X.shape = (1, (- 1))
    if (ndmin not in [0, 1, 2]):
        raise ValueError(('Illegal value of ndmin keyword: %s' % ndmin))
    if (X.ndim > ndmin):
        X = np.squeeze(X)
    if (X.ndim < ndmin):
        if (ndmin == 1):
            X = np.atleast_1d(X)
        elif (ndmin == 2):
            X = np.atleast_2d(X).T
    if unpack:
        if (len(dtype_types) > 1):
            return [X[field] for field in dtype.names]
        else:
            return X.T
    else:
        return X