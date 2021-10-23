@set_module('numpy')
def loadtxt(fname, dtype=float, comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0, encoding='bytes', max_rows=None):
    '\n    Load data from a text file.\n\n    Each row in the text file must have the same number of values.\n\n    Parameters\n    ----------\n    fname : file, str, or pathlib.Path\n        File, filename, or generator to read.  If the filename extension is\n        ``.gz`` or ``.bz2``, the file is first decompressed. Note that\n        generators should return byte strings.\n    dtype : data-type, optional\n        Data-type of the resulting array; default: float.  If this is a\n        structured data-type, the resulting array will be 1-dimensional, and\n        each row will be interpreted as an element of the array.  In this\n        case, the number of columns used must match the number of fields in\n        the data-type.\n    comments : str or sequence of str, optional\n        The characters or list of characters used to indicate the start of a\n        comment. None implies no comments. For backwards compatibility, byte\n        strings will be decoded as \'latin1\'. The default is \'#\'.\n    delimiter : str, optional\n        The string used to separate values. For backwards compatibility, byte\n        strings will be decoded as \'latin1\'. The default is whitespace.\n    converters : dict, optional\n        A dictionary mapping column number to a function that will parse the\n        column string into the desired value.  E.g., if column 0 is a date\n        string: ``converters = {0: datestr2num}``.  Converters can also be\n        used to provide a default value for missing data (but see also\n        `genfromtxt`): ``converters = {3: lambda s: float(s.strip() or 0)}``.\n        Default: None.\n    skiprows : int, optional\n        Skip the first `skiprows` lines, including comments; default: 0.\n    usecols : int or sequence, optional\n        Which columns to read, with 0 being the first. For example,\n        ``usecols = (1,4,5)`` will extract the 2nd, 5th and 6th columns.\n        The default, None, results in all columns being read.\n\n        .. versionchanged:: 1.11.0\n            When a single column has to be read it is possible to use\n            an integer instead of a tuple. E.g ``usecols = 3`` reads the\n            fourth column the same way as ``usecols = (3,)`` would.\n    unpack : bool, optional\n        If True, the returned array is transposed, so that arguments may be\n        unpacked using ``x, y, z = loadtxt(...)``.  When used with a structured\n        data-type, arrays are returned for each field.  Default is False.\n    ndmin : int, optional\n        The returned array will have at least `ndmin` dimensions.\n        Otherwise mono-dimensional axes will be squeezed.\n        Legal values: 0 (default), 1 or 2.\n\n        .. versionadded:: 1.6.0\n    encoding : str, optional\n        Encoding used to decode the inputfile. Does not apply to input streams.\n        The special value \'bytes\' enables backward compatibility workarounds\n        that ensures you receive byte arrays as results if possible and passes\n        \'latin1\' encoded strings to converters. Override this value to receive\n        unicode arrays and pass strings as input to converters.  If set to None\n        the system default is used. The default value is \'bytes\'.\n\n        .. versionadded:: 1.14.0\n    max_rows : int, optional\n        Read `max_rows` lines of content after `skiprows` lines. The default\n        is to read all the lines.\n\n        .. versionadded:: 1.16.0\n\n    Returns\n    -------\n    out : ndarray\n        Data read from the text file.\n\n    See Also\n    --------\n    load, fromstring, fromregex\n    genfromtxt : Load data with missing values handled as specified.\n    scipy.io.loadmat : reads MATLAB data files\n\n    Notes\n    -----\n    This function aims to be a fast reader for simply formatted files.  The\n    `genfromtxt` function provides more sophisticated handling of, e.g.,\n    lines with missing values.\n\n    .. versionadded:: 1.10.0\n\n    The strings produced by the Python float.hex method can be used as\n    input for floats.\n\n    Examples\n    --------\n    >>> from io import StringIO   # StringIO behaves like a file object\n    >>> c = StringIO(u"0 1\\n2 3")\n    >>> np.loadtxt(c)\n    array([[0., 1.],\n           [2., 3.]])\n\n    >>> d = StringIO(u"M 21 72\\nF 35 58")\n    >>> np.loadtxt(d, dtype={\'names\': (\'gender\', \'age\', \'weight\'),\n    ...                      \'formats\': (\'S1\', \'i4\', \'f4\')})\n    array([(b\'M\', 21, 72.), (b\'F\', 35, 58.)],\n          dtype=[(\'gender\', \'S1\'), (\'age\', \'<i4\'), (\'weight\', \'<f4\')])\n\n    >>> c = StringIO(u"1,0,2\\n3,0,4")\n    >>> x, y = np.loadtxt(c, delimiter=\',\', usecols=(0, 2), unpack=True)\n    >>> x\n    array([1., 3.])\n    >>> y\n    array([2., 4.])\n\n    '
    if (comments is not None):
        if isinstance(comments, (basestring, bytes)):
            comments = [comments]
        comments = [_decode_line(x) for x in comments]
        comments = (re.escape(comment) for comment in comments)
        regex_comments = re.compile('|'.join(comments))
    if (delimiter is not None):
        delimiter = _decode_line(delimiter)
    user_converters = converters
    if (encoding == 'bytes'):
        encoding = None
        byte_converters = True
    else:
        byte_converters = False
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
        if isinstance(fname, os_PathLike):
            fname = os_fspath(fname)
        if _is_string_like(fname):
            fh = np.lib._datasource.open(fname, 'rt', encoding=encoding)
            fencoding = getattr(fh, 'encoding', 'latin1')
            fh = iter(fh)
            fown = True
        else:
            fh = iter(fname)
            fencoding = getattr(fname, 'encoding', 'latin1')
    except TypeError:
        raise ValueError('fname must be a string, file handle, or generator')
    if (encoding is not None):
        fencoding = encoding
    elif (fencoding is None):
        import locale
        fencoding = locale.getpreferredencoding()

    @recursive
    def flatten_dtype_internal(self, dt):
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
                (flat_dt, flat_packing) = self(tp)
                types.extend(flat_dt)
                if (tp.ndim > 0):
                    packing.extend(flat_packing)
                else:
                    packing.append((len(flat_dt), flat_packing))
            return (types, packing)

    @recursive
    def pack_items(self, items, packing):
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
                ret.append(self(items[start:(start + length)], subpacking))
                start += length
            return tuple(ret)

    def split_line(line):
        'Chop off comments, strip, and split at delimiter. '
        line = _decode_line(line, encoding=encoding)
        if (comments is not None):
            line = regex_comments.split(line, maxsplit=1)[0]
        line = line.strip('\r\n')
        if line:
            return line.split(delimiter)
        else:
            return []

    def read_data(chunk_size):
        'Parse each line, including the first.\n\n        The file read, `fh`, is a global defined above.\n\n        Parameters\n        ----------\n        chunk_size : int\n            At most `chunk_size` lines are read at a time, with iteration\n            until all lines are read.\n\n        '
        X = []
        line_iter = itertools.chain([first_line], fh)
        line_iter = itertools.islice(line_iter, max_rows)
        for (i, line) in enumerate(line_iter):
            vals = split_line(line)
            if (len(vals) == 0):
                continue
            if usecols:
                vals = [vals[j] for j in usecols]
            if (len(vals) != N):
                line_num = ((i + skiprows) + 1)
                raise ValueError(('Wrong number of columns at line %d' % line_num))
            items = [conv(val) for (conv, val) in zip(converters, vals)]
            items = pack_items(items, packing)
            X.append(items)
            if (len(X) > chunk_size):
                (yield X)
                X = []
        if X:
            (yield X)
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
            warnings.warn(('loadtxt: Empty input file: "%s"' % fname), stacklevel=2)
        N = len((usecols or first_vals))
        (dtype_types, packing) = flatten_dtype_internal(dtype)
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
            if byte_converters:

                def tobytes_first(x, conv):
                    if (type(x) is bytes):
                        return conv(x)
                    return conv(x.encode('latin1'))
                converters[i] = functools.partial(tobytes_first, conv=conv)
            else:
                converters[i] = conv
        converters = [(conv if (conv is not bytes) else (lambda x: x.encode(fencoding))) for conv in converters]
        X = None
        for x in read_data(_loadtxt_chunksize):
            if (X is None):
                X = np.array(x, dtype)
            else:
                nshape = list(X.shape)
                pos = nshape[0]
                nshape[0] += len(x)
                X.resize(nshape, refcheck=False)
                X[pos:, ...] = x
    finally:
        if fown:
            fh.close()
    if (X is None):
        X = np.array([], dtype)
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