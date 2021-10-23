def _write(self, stream, a, comment='', field=None, precision=None, symmetry=None):
    if (isinstance(a, list) or isinstance(a, ndarray) or isinstance(a, tuple) or hasattr(a, '__array__')):
        rep = self.FORMAT_ARRAY
        a = asarray(a)
        if (len(a.shape) != 2):
            raise ValueError('Expected 2 dimensional array')
        (rows, cols) = a.shape
        if (field is not None):
            if (field == self.FIELD_INTEGER):
                if (not can_cast(a.dtype, 'intp')):
                    raise OverflowError("mmwrite does not support integer dtypes larger than native 'intp'.")
                a = a.astype('intp')
            elif (field == self.FIELD_REAL):
                if (a.dtype.char not in 'fd'):
                    a = a.astype('d')
            elif (field == self.FIELD_COMPLEX):
                if (a.dtype.char not in 'FD'):
                    a = a.astype('D')
    else:
        if (not isspmatrix(a)):
            raise ValueError(('unknown matrix type: %s' % type(a)))
        rep = 'coordinate'
        (rows, cols) = a.shape
    typecode = a.dtype.char
    if (precision is None):
        if (typecode in 'fF'):
            precision = 8
        else:
            precision = 16
    if (field is None):
        kind = a.dtype.kind
        if (kind == 'i'):
            if (not can_cast(a.dtype, 'intp')):
                raise OverflowError("mmwrite does not support integer dtypes larger than native 'intp'.")
            field = 'integer'
        elif (kind == 'f'):
            field = 'real'
        elif (kind == 'c'):
            field = 'complex'
        else:
            raise TypeError(('unexpected dtype kind ' + kind))
    if (symmetry is None):
        symmetry = self._get_symmetry(a)
    self.__class__._validate_format(rep)
    self.__class__._validate_field(field)
    self.__class__._validate_symmetry(symmetry)
    stream.write(asbytes('%%MatrixMarket matrix {0} {1} {2}\n'.format(rep, field, symmetry)))
    for line in comment.split('\n'):
        stream.write(asbytes(('%%%s\n' % line)))
    template = self._field_template(field, precision)
    if (rep == self.FORMAT_ARRAY):
        stream.write(asbytes(('%i %i\n' % (rows, cols))))
        if (field in (self.FIELD_INTEGER, self.FIELD_REAL)):
            if (symmetry == self.SYMMETRY_GENERAL):
                for j in range(cols):
                    for i in range(rows):
                        stream.write(asbytes((template % a[(i, j)])))
            else:
                for j in range(cols):
                    for i in range(j, rows):
                        stream.write(asbytes((template % a[(i, j)])))
        elif (field == self.FIELD_COMPLEX):
            if (symmetry == self.SYMMETRY_GENERAL):
                for j in range(cols):
                    for i in range(rows):
                        aij = a[(i, j)]
                        stream.write(asbytes((template % (real(aij), imag(aij)))))
            else:
                for j in range(cols):
                    for i in range(j, rows):
                        aij = a[(i, j)]
                        stream.write(asbytes((template % (real(aij), imag(aij)))))
        elif (field == self.FIELD_PATTERN):
            raise ValueError('pattern type inconsisted with dense format')
        else:
            raise TypeError(('Unknown field type %s' % field))
    else:
        coo = a.tocoo()
        if (symmetry != self.SYMMETRY_GENERAL):
            lower_triangle_mask = (coo.row >= coo.col)
            coo = coo_matrix((coo.data[lower_triangle_mask], (coo.row[lower_triangle_mask], coo.col[lower_triangle_mask])), shape=coo.shape)
        stream.write(asbytes(('%i %i %i\n' % (rows, cols, coo.nnz))))
        template = self._field_template(field, (precision - 1))
        if (field == self.FIELD_PATTERN):
            for (r, c) in zip((coo.row + 1), (coo.col + 1)):
                stream.write(asbytes(('%i %i\n' % (r, c))))
        elif (field in (self.FIELD_INTEGER, self.FIELD_REAL)):
            for (r, c, d) in zip((coo.row + 1), (coo.col + 1), coo.data):
                stream.write(asbytes((('%i %i ' % (r, c)) + (template % d))))
        elif (field == self.FIELD_COMPLEX):
            for (r, c, d) in zip((coo.row + 1), (coo.col + 1), coo.data):
                stream.write(asbytes((('%i %i ' % (r, c)) + (template % (d.real, d.imag)))))
        else:
            raise TypeError(('Unknown field type %s' % field))