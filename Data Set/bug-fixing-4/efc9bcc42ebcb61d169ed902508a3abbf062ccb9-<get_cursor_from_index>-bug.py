def get_cursor_from_index(self, index):
    'Return the (row, col) of the cursor from text index.\n        '
    index = boundary(index, 0, len(self.text))
    if (index <= 0):
        return (0, 0)
    lf = self._lines_flags
    l = self._lines
    i = 0
    for row in range(len(l)):
        ni = (i + len(l[row]))
        if (lf[row] & FL_IS_LINEBREAK):
            ni += 1
            i += 1
        if (ni >= index):
            return ((index - i), row)
        i = ni
    return (index, row)