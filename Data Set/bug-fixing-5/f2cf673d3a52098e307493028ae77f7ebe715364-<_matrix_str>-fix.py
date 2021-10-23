def _matrix_str(self, indent=''):
    (fmt, scale, sz) = _number_format(self)
    nColumnPerLine = int(math.floor(((80 - len(indent)) / (sz + 1))))
    strt = ''
    firstColumn = 0
    while (firstColumn < self.size(1)):
        lastColumn = min(((firstColumn + nColumnPerLine) - 1), (self.size(1) - 1))
        if (nColumnPerLine < self.size(1)):
            strt += ('\n' if (firstColumn != 1) else '')
            strt += 'Columns {} to {} \n{}'.format(firstColumn, lastColumn, indent)
        if (scale != 1):
            strt += SCALE_FORMAT.format(scale)
        for l in _range(self.size(0)):
            strt += (indent + (' ' if (scale != 1) else ''))
            row_slice = self[l, firstColumn:(lastColumn + 1)]
            strt += (' '.join((fmt.format((val / scale)) for val in row_slice)) + '\n')
        firstColumn = (lastColumn + 1)
    return strt