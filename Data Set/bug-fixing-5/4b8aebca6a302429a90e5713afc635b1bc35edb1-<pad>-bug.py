def pad(mat, padrow, padcol):
    '\n    Add additional rows/columns to a np.matrix `mat`. The new rows/columns\n    will be initialized with zeros.\n    '
    if (padrow < 0):
        padrow = 0
    if (padcol < 0):
        padcol = 0
    (rows, cols) = mat.shape
    return np.bmat([[mat, np.matrix(np.zeros((rows, padcol)))], [np.matrix(np.zeros((padrow, (cols + padcol))))]])