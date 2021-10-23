def _parse_body(self, stream):
    (rows, cols, entries, format, field, symm) = (self.rows, self.cols, self.entries, self.format, self.field, self.symmetry)
    try:
        from scipy.sparse import coo_matrix
    except ImportError:
        coo_matrix = None
    dtype = self.DTYPES_BY_FIELD.get(field, None)
    has_symmetry = self.has_symmetry
    is_integer = (field == self.FIELD_INTEGER)
    is_complex = (field == self.FIELD_COMPLEX)
    is_skew = (symm == self.SYMMETRY_SKEW_SYMMETRIC)
    is_herm = (symm == self.SYMMETRY_HERMITIAN)
    is_pattern = (field == self.FIELD_PATTERN)
    if (format == self.FORMAT_ARRAY):
        a = zeros((rows, cols), dtype=dtype)
        line = 1
        (i, j) = (0, 0)
        while line:
            line = stream.readline()
            if ((not line) or line.startswith(b'%')):
                continue
            if is_integer:
                aij = int(line)
            elif is_complex:
                aij = complex(*map(float, line.split()))
            else:
                aij = float(line)
            a[(i, j)] = aij
            if (has_symmetry and (i != j)):
                if is_skew:
                    a[(j, i)] = (- aij)
                elif is_herm:
                    a[(j, i)] = conj(aij)
                else:
                    a[(j, i)] = aij
            if (i < (rows - 1)):
                i = (i + 1)
            else:
                j = (j + 1)
                if (not has_symmetry):
                    i = 0
                else:
                    i = j
        if (not ((i in [0, j]) and (j == cols))):
            raise ValueError('Parse error, did not read all lines.')
    elif ((format == self.FORMAT_COORDINATE) and (coo_matrix is None)):
        a = zeros((rows, cols), dtype=dtype)
        line = 1
        k = 0
        while line:
            line = stream.readline()
            if ((not line) or line.startswith(b'%')):
                continue
            l = line.split()
            (i, j) = map(int, l[:2])
            (i, j) = ((i - 1), (j - 1))
            if is_integer:
                aij = int(l[2])
            elif is_complex:
                aij = complex(*map(float, l[2:]))
            else:
                aij = float(l[2])
            a[(i, j)] = aij
            if (has_symmetry and (i != j)):
                if is_skew:
                    a[(j, i)] = (- aij)
                elif is_herm:
                    a[(j, i)] = conj(aij)
                else:
                    a[(j, i)] = aij
            k = (k + 1)
        if (not (k == entries)):
            ValueError('Did not read all entries')
    elif (format == self.FORMAT_COORDINATE):
        if (entries == 0):
            return coo_matrix((rows, cols), dtype=dtype)
        I = zeros(entries, dtype='intc')
        J = zeros(entries, dtype='intc')
        if is_pattern:
            V = ones(entries, dtype='int8')
        elif is_integer:
            V = zeros(entries, dtype='int')
        elif is_complex:
            V = zeros(entries, dtype='complex')
        else:
            V = zeros(entries, dtype='float')
        entry_number = 0
        for line in stream:
            if ((not line) or line.startswith(b'%')):
                continue
            if ((entry_number + 1) > entries):
                raise ValueError("'entries' in header is smaller than number of entries")
            l = line.split()
            (I[entry_number], J[entry_number]) = map(int, l[:2])
            if (not is_pattern):
                if is_integer:
                    V[entry_number] = int(l[2])
                elif is_complex:
                    V[entry_number] = complex(*map(float, l[2:]))
                else:
                    V[entry_number] = float(l[2])
            entry_number += 1
        if (entry_number < entries):
            raise ValueError("'entries' in header is larger than number of entries")
        I -= 1
        J -= 1
        if has_symmetry:
            mask = (I != J)
            od_I = I[mask]
            od_J = J[mask]
            od_V = V[mask]
            I = concatenate((I, od_J))
            J = concatenate((J, od_I))
            if is_skew:
                od_V *= (- 1)
            elif is_herm:
                od_V = od_V.conjugate()
            V = concatenate((V, od_V))
        a = coo_matrix((V, (I, J)), shape=(rows, cols), dtype=dtype)
    else:
        raise NotImplementedError(format)
    return a