

def genfromtxt(fname, dtype=float, comments='#', delimiter=None, skip_header=0, skip_footer=0, converters=None, missing_values=None, filling_values=None, usecols=None, names=None, excludelist=None, deletechars=None, replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None, usemask=False, loose=True, invalid_raise=True, max_rows=None):
    '\n    Load data from a text file, with missing values handled as specified.\n\n    Each line past the first `skip_header` lines is split at the `delimiter`\n    character, and characters following the `comments` character are discarded.\n\n    Parameters\n    ----------\n    fname : file, str, pathlib.Path, list of str, generator\n        File, filename, list, or generator to read.  If the filename\n        extension is `.gz` or `.bz2`, the file is first decompressed. Note\n        that generators must return byte strings in Python 3k.  The strings\n        in a list or produced by a generator are treated as lines.\n    dtype : dtype, optional\n        Data type of the resulting array.\n        If None, the dtypes will be determined by the contents of each\n        column, individually.\n    comments : str, optional\n        The character used to indicate the start of a comment.\n        All the characters occurring on a line after a comment are discarded\n    delimiter : str, int, or sequence, optional\n        The string used to separate values.  By default, any consecutive\n        whitespaces act as delimiter.  An integer or sequence of integers\n        can also be provided as width(s) of each field.\n    skiprows : int, optional\n        `skiprows` was removed in numpy 1.10. Please use `skip_header` instead.\n    skip_header : int, optional\n        The number of lines to skip at the beginning of the file.\n    skip_footer : int, optional\n        The number of lines to skip at the end of the file.\n    converters : variable, optional\n        The set of functions that convert the data of a column to a value.\n        The converters can also be used to provide a default value\n        for missing data: ``converters = {3: lambda s: float(s or 0)}``.\n    missing : variable, optional\n        `missing` was removed in numpy 1.10. Please use `missing_values`\n        instead.\n    missing_values : variable, optional\n        The set of strings corresponding to missing data.\n    filling_values : variable, optional\n        The set of values to be used as default when the data are missing.\n    usecols : sequence, optional\n        Which columns to read, with 0 being the first.  For example,\n        ``usecols = (1, 4, 5)`` will extract the 2nd, 5th and 6th columns.\n    names : {None, True, str, sequence}, optional\n        If `names` is True, the field names are read from the first valid line\n        after the first `skip_header` lines.\n        If `names` is a sequence or a single-string of comma-separated names,\n        the names will be used to define the field names in a structured dtype.\n        If `names` is None, the names of the dtype fields will be used, if any.\n    excludelist : sequence, optional\n        A list of names to exclude. This list is appended to the default list\n        [\'return\',\'file\',\'print\']. Excluded names are appended an underscore:\n        for example, `file` would become `file_`.\n    deletechars : str, optional\n        A string combining invalid characters that must be deleted from the\n        names.\n    defaultfmt : str, optional\n        A format used to define default field names, such as "f%i" or "f_%02i".\n    autostrip : bool, optional\n        Whether to automatically strip white spaces from the variables.\n    replace_space : char, optional\n        Character(s) used in replacement of white spaces in the variables\n        names. By default, use a \'_\'.\n    case_sensitive : {True, False, \'upper\', \'lower\'}, optional\n        If True, field names are case sensitive.\n        If False or \'upper\', field names are converted to upper case.\n        If \'lower\', field names are converted to lower case.\n    unpack : bool, optional\n        If True, the returned array is transposed, so that arguments may be\n        unpacked using ``x, y, z = loadtxt(...)``\n    usemask : bool, optional\n        If True, return a masked array.\n        If False, return a regular array.\n    loose : bool, optional\n        If True, do not raise errors for invalid values.\n    invalid_raise : bool, optional\n        If True, an exception is raised if an inconsistency is detected in the\n        number of columns.\n        If False, a warning is emitted and the offending lines are skipped.\n    max_rows : int,  optional\n        The maximum number of rows to read. Must not be used with skip_footer\n        at the same time.  If given, the value must be at least 1. Default is\n        to read the entire file.\n\n        .. versionadded:: 1.10.0\n\n    Returns\n    -------\n    out : ndarray\n        Data read from the text file. If `usemask` is True, this is a\n        masked array.\n\n    See Also\n    --------\n    numpy.loadtxt : equivalent function when no data is missing.\n\n    Notes\n    -----\n    * When spaces are used as delimiters, or when no delimiter has been given\n      as input, there should not be any missing data between two fields.\n    * When the variables are named (either by a flexible dtype or with `names`,\n      there must not be any header in the file (else a ValueError\n      exception is raised).\n    * Individual values are not stripped of spaces by default.\n      When using a custom converter, make sure the function does remove spaces.\n\n    References\n    ----------\n    .. [1] NumPy User Guide, section `I/O with NumPy\n           <http://docs.scipy.org/doc/numpy/user/basics.io.genfromtxt.html>`_.\n\n    Examples\n    ---------\n    >>> from io import StringIO\n    >>> import numpy as np\n\n    Comma delimited file with mixed dtype\n\n    >>> s = StringIO("1,1.3,abcde")\n    >>> data = np.genfromtxt(s, dtype=[(\'myint\',\'i8\'),(\'myfloat\',\'f8\'),\n    ... (\'mystring\',\'S5\')], delimiter=",")\n    >>> data\n    array((1, 1.3, \'abcde\'),\n          dtype=[(\'myint\', \'<i8\'), (\'myfloat\', \'<f8\'), (\'mystring\', \'|S5\')])\n\n    Using dtype = None\n\n    >>> s.seek(0) # needed for StringIO example only\n    >>> data = np.genfromtxt(s, dtype=None,\n    ... names = [\'myint\',\'myfloat\',\'mystring\'], delimiter=",")\n    >>> data\n    array((1, 1.3, \'abcde\'),\n          dtype=[(\'myint\', \'<i8\'), (\'myfloat\', \'<f8\'), (\'mystring\', \'|S5\')])\n\n    Specifying dtype and names\n\n    >>> s.seek(0)\n    >>> data = np.genfromtxt(s, dtype="i8,f8,S5",\n    ... names=[\'myint\',\'myfloat\',\'mystring\'], delimiter=",")\n    >>> data\n    array((1, 1.3, \'abcde\'),\n          dtype=[(\'myint\', \'<i8\'), (\'myfloat\', \'<f8\'), (\'mystring\', \'|S5\')])\n\n    An example with fixed-width columns\n\n    >>> s = StringIO("11.3abcde")\n    >>> data = np.genfromtxt(s, dtype=None, names=[\'intvar\',\'fltvar\',\'strvar\'],\n    ...     delimiter=[1,3,5])\n    >>> data\n    array((1, 1.3, \'abcde\'),\n          dtype=[(\'intvar\', \'<i8\'), (\'fltvar\', \'<f8\'), (\'strvar\', \'|S5\')])\n\n    '
    if (max_rows is not None):
        if skip_footer:
            raise ValueError("The keywords 'skip_footer' and 'max_rows' can not be specified at the same time.")
        if (max_rows < 1):
            raise ValueError("'max_rows' must be at least 1.")
    if (comments is not None):
        comments = asbytes(comments)
    if isinstance(delimiter, unicode):
        delimiter = asbytes(delimiter)
    if isinstance(missing_values, (unicode, list, tuple)):
        missing_values = asbytes_nested(missing_values)
    if usemask:
        from numpy.ma import MaskedArray, make_mask_descr
    user_converters = (converters or {
        
    })
    if (not isinstance(user_converters, dict)):
        raise TypeError(("The input argument 'converter' should be a valid dictionary (got '%s' instead)" % type(user_converters)))
    own_fhd = False
    try:
        if is_pathlib_path(fname):
            fname = str(fname)
        if isinstance(fname, basestring):
            if (sys.version_info[0] == 2):
                fhd = iter(np.lib._datasource.open(fname, 'rbU'))
            else:
                fhd = iter(np.lib._datasource.open(fname, 'rb'))
            own_fhd = True
        else:
            fhd = iter(fname)
    except TypeError:
        raise TypeError(('fname must be a string, filehandle, list of strings, or generator. Got %s instead.' % type(fname)))
    split_line = LineSplitter(delimiter=delimiter, comments=comments, autostrip=autostrip)._handyman
    validate_names = NameValidator(excludelist=excludelist, deletechars=deletechars, case_sensitive=case_sensitive, replace_space=replace_space)
    for i in range(skip_header):
        next(fhd)
    first_values = None
    try:
        while (not first_values):
            first_line = next(fhd)
            if (names is True):
                if (comments in first_line):
                    first_line = asbytes('').join(first_line.split(comments)[1:])
            first_values = split_line(first_line)
    except StopIteration:
        first_line = asbytes('')
        first_values = []
        warnings.warn(('genfromtxt: Empty input file: "%s"' % fname), stacklevel=2)
    if (names is True):
        fval = first_values[0].strip()
        if (fval in comments):
            del first_values[0]
    if (usecols is not None):
        try:
            usecols = [_.strip() for _ in usecols.split(',')]
        except AttributeError:
            try:
                usecols = list(usecols)
            except TypeError:
                usecols = [usecols]
    nbcols = len((usecols or first_values))
    if (names is True):
        names = validate_names([_bytes_to_name(_.strip()) for _ in first_values])
        first_line = asbytes('')
    elif _is_string_like(names):
        names = validate_names([_.strip() for _ in names.split(',')])
    elif names:
        names = validate_names(names)
    if (dtype is not None):
        dtype = easy_dtype(dtype, defaultfmt=defaultfmt, names=names, excludelist=excludelist, deletechars=deletechars, case_sensitive=case_sensitive, replace_space=replace_space)
    if (names is not None):
        names = list(names)
    if usecols:
        for (i, current) in enumerate(usecols):
            if _is_string_like(current):
                usecols[i] = names.index(current)
            elif (current < 0):
                usecols[i] = (current + len(first_values))
        if ((dtype is not None) and (len(dtype) > nbcols)):
            descr = dtype.descr
            dtype = np.dtype([descr[_] for _ in usecols])
            names = list(dtype.names)
        elif ((names is not None) and (len(names) > nbcols)):
            names = [names[_] for _ in usecols]
    elif ((names is not None) and (dtype is not None)):
        names = list(dtype.names)
    user_missing_values = (missing_values or ())
    missing_values = [list([asbytes('')]) for _ in range(nbcols)]
    if isinstance(user_missing_values, dict):
        for (key, val) in user_missing_values.items():
            if _is_string_like(key):
                try:
                    key = names.index(key)
                except ValueError:
                    continue
            if usecols:
                try:
                    key = usecols.index(key)
                except ValueError:
                    pass
            if isinstance(val, (list, tuple)):
                val = [str(_) for _ in val]
            else:
                val = [str(val)]
            if (key is None):
                for miss in missing_values:
                    miss.extend(val)
            else:
                missing_values[key].extend(val)
    elif isinstance(user_missing_values, (list, tuple)):
        for (value, entry) in zip(user_missing_values, missing_values):
            value = str(value)
            if (value not in entry):
                entry.append(value)
    elif isinstance(user_missing_values, bytes):
        user_value = user_missing_values.split(asbytes(','))
        for entry in missing_values:
            entry.extend(user_value)
    else:
        for entry in missing_values:
            entry.extend([str(user_missing_values)])
    user_filling_values = filling_values
    if (user_filling_values is None):
        user_filling_values = []
    filling_values = ([None] * nbcols)
    if isinstance(user_filling_values, dict):
        for (key, val) in user_filling_values.items():
            if _is_string_like(key):
                try:
                    key = names.index(key)
                except ValueError:
                    continue
            if usecols:
                try:
                    key = usecols.index(key)
                except ValueError:
                    pass
            filling_values[key] = val
    elif isinstance(user_filling_values, (list, tuple)):
        n = len(user_filling_values)
        if (n <= nbcols):
            filling_values[:n] = user_filling_values
        else:
            filling_values = user_filling_values[:nbcols]
    else:
        filling_values = ([user_filling_values] * nbcols)
    if (dtype is None):
        converters = [StringConverter(None, missing_values=miss, default=fill) for (miss, fill) in zip(missing_values, filling_values)]
    else:
        dtype_flat = flatten_dtype(dtype, flatten_base=True)
        if (len(dtype_flat) > 1):
            zipit = zip(dtype_flat, missing_values, filling_values)
            converters = [StringConverter(dt, locked=True, missing_values=miss, default=fill) for (dt, miss, fill) in zipit]
        else:
            zipit = zip(missing_values, filling_values)
            converters = [StringConverter(dtype, locked=True, missing_values=miss, default=fill) for (miss, fill) in zipit]
    uc_update = []
    for (j, conv) in user_converters.items():
        if _is_string_like(j):
            try:
                j = names.index(j)
                i = j
            except ValueError:
                continue
        elif usecols:
            try:
                i = usecols.index(j)
            except ValueError:
                continue
        else:
            i = j
        if len(first_line):
            testing_value = first_values[j]
        else:
            testing_value = None
        converters[i].update(conv, locked=True, testing_value=testing_value, default=filling_values[i], missing_values=missing_values[i])
        uc_update.append((i, conv))
    user_converters.update(uc_update)
    rows = []
    append_to_rows = rows.append
    if usemask:
        masks = []
        append_to_masks = masks.append
    invalid = []
    append_to_invalid = invalid.append
    for (i, line) in enumerate(itertools.chain([first_line], fhd)):
        values = split_line(line)
        nbvalues = len(values)
        if (nbvalues == 0):
            continue
        if usecols:
            try:
                values = [values[_] for _ in usecols]
            except IndexError:
                append_to_invalid((((i + skip_header) + 1), nbvalues))
                continue
        elif (nbvalues != nbcols):
            append_to_invalid((((i + skip_header) + 1), nbvalues))
            continue
        append_to_rows(tuple(values))
        if usemask:
            append_to_masks(tuple([(v.strip() in m) for (v, m) in zip(values, missing_values)]))
        if (len(rows) == max_rows):
            break
    if own_fhd:
        fhd.close()
    if (dtype is None):
        for (i, converter) in enumerate(converters):
            current_column = [itemgetter(i)(_m) for _m in rows]
            try:
                converter.iterupgrade(current_column)
            except ConverterLockError:
                errmsg = ('Converter #%i is locked and cannot be upgraded: ' % i)
                current_column = map(itemgetter(i), rows)
                for (j, value) in enumerate(current_column):
                    try:
                        converter.upgrade(value)
                    except (ConverterError, ValueError):
                        errmsg += "(occurred line #%i for value '%s')"
                        errmsg %= (((j + 1) + skip_header), value)
                        raise ConverterError(errmsg)
    nbinvalid = len(invalid)
    if (nbinvalid > 0):
        nbrows = ((len(rows) + nbinvalid) - skip_footer)
        template = ('    Line #%%i (got %%i columns instead of %i)' % nbcols)
        if (skip_footer > 0):
            nbinvalid_skipped = len([_ for _ in invalid if (_[0] > (nbrows + skip_header))])
            invalid = invalid[:(nbinvalid - nbinvalid_skipped)]
            skip_footer -= nbinvalid_skipped
        errmsg = [(template % (i, nb)) for (i, nb) in invalid]
        if len(errmsg):
            errmsg.insert(0, 'Some errors were detected !')
            errmsg = '\n'.join(errmsg)
            if invalid_raise:
                raise ValueError(errmsg)
            else:
                warnings.warn(errmsg, ConversionWarning, stacklevel=2)
    if (skip_footer > 0):
        rows = rows[:(- skip_footer)]
        if usemask:
            masks = masks[:(- skip_footer)]
    if loose:
        rows = list(zip(*[[conv._loose_call(_r) for _r in map(itemgetter(i), rows)] for (i, conv) in enumerate(converters)]))
    else:
        rows = list(zip(*[[conv._strict_call(_r) for _r in map(itemgetter(i), rows)] for (i, conv) in enumerate(converters)]))
    data = rows
    if (dtype is None):
        column_types = [conv.type for conv in converters]
        strcolidx = [i for (i, v) in enumerate(column_types) if (v in (type('S'), np.string_))]
        for i in strcolidx:
            column_types[i] = ('|S%i' % max((len(row[i]) for row in data)))
        if (names is None):
            base = set([c.type for c in converters if c._checked])
            if (len(base) == 1):
                (ddtype, mdtype) = (list(base)[0], np.bool)
            else:
                ddtype = [((defaultfmt % i), dt) for (i, dt) in enumerate(column_types)]
                if usemask:
                    mdtype = [((defaultfmt % i), np.bool) for (i, dt) in enumerate(column_types)]
        else:
            ddtype = list(zip(names, column_types))
            mdtype = list(zip(names, ([np.bool] * len(column_types))))
        output = np.array(data, dtype=ddtype)
        if usemask:
            outputmask = np.array(masks, dtype=mdtype)
    else:
        if (names and dtype.names):
            dtype.names = names
        if (len(dtype_flat) > 1):
            if ('O' in (_.char for _ in dtype_flat)):
                if has_nested_fields(dtype):
                    raise NotImplementedError('Nested fields involving objects are not supported...')
                else:
                    output = np.array(data, dtype=dtype)
            else:
                rows = np.array(data, dtype=[('', _) for _ in dtype_flat])
                output = rows.view(dtype)
            if usemask:
                rowmasks = np.array(masks, dtype=np.dtype([('', np.bool) for t in dtype_flat]))
                mdtype = make_mask_descr(dtype)
                outputmask = rowmasks.view(mdtype)
        else:
            if user_converters:
                ishomogeneous = True
                descr = []
                for (i, ttype) in enumerate([conv.type for conv in converters]):
                    if (i in user_converters):
                        ishomogeneous &= (ttype == dtype.type)
                        if (ttype == np.string_):
                            ttype = ('|S%i' % max((len(row[i]) for row in data)))
                        descr.append(('', ttype))
                    else:
                        descr.append(('', dtype))
                if (not ishomogeneous):
                    if (len(descr) > 1):
                        dtype = np.dtype(descr)
                    else:
                        dtype = np.dtype(ttype)
            output = np.array(data, dtype)
            if usemask:
                if dtype.names:
                    mdtype = [(_, np.bool) for _ in dtype.names]
                else:
                    mdtype = np.bool
                outputmask = np.array(masks, dtype=mdtype)
    names = output.dtype.names
    if (usemask and names):
        for (name, conv) in zip((names or ()), converters):
            missing_values = [conv(_) for _ in conv.missing_values if (_ != asbytes(''))]
            for mval in missing_values:
                outputmask[name] |= (output[name] == mval)
    if usemask:
        output = output.view(MaskedArray)
        output._mask = outputmask
    if unpack:
        return output.squeeze().T
    return output.squeeze()
