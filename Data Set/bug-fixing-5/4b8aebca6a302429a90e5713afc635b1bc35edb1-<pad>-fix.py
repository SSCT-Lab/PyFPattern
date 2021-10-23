def pad(mat, padrow, padcol):
    'Add additional rows/columns to `mat`. The new rows/columns will be initialized with zeros.\n\n    Parameters\n    ----------\n    mat : numpy.ndarray\n        Input 2D matrix\n    padrow : int\n        Number of additional rows\n    padcol : int\n        Number of additional columns\n\n    Returns\n    -------\n    numpy.matrixlib.defmatrix.matrix\n        Matrix with needed padding.\n\n    '
    if (padrow < 0):
        padrow = 0
    if (padcol < 0):
        padcol = 0
    (rows, cols) = mat.shape
    return np.bmat([[mat, np.matrix(np.zeros((rows, padcol)))], [np.matrix(np.zeros((padrow, (cols + padcol))))]])