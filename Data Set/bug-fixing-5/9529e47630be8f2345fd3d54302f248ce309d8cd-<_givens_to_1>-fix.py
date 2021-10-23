def _givens_to_1(self, aii, ajj, aij):
    "Computes a 2x2 Givens matrix to put 1's on the diagonal.\n\n        The input matrix is a 2x2 symmetric matrix M = [ aii aij ; aij ajj ].\n\n        The output matrix g is a 2x2 anti-symmetric matrix of the form\n        [ c s ; -s c ];  the elements c and s are returned.\n\n        Applying the output matrix to the input matrix (as b=g.T M g)\n        results in a matrix with bii=1, provided tr(M) - det(M) >= 1\n        and floating point issues do not occur. Otherwise, some other\n        valid rotation is returned. When tr(M)==2, also bjj=1.\n\n        "
    aiid = (aii - 1.0)
    ajjd = (ajj - 1.0)
    if (ajjd == 0):
        return (0.0, 1.0)
    dd = math.sqrt(max(((aij ** 2) - (aiid * ajjd)), 0))
    t = ((aij + math.copysign(dd, aij)) / ajjd)
    c = (1.0 / math.sqrt((1.0 + (t * t))))
    if (c == 0):
        s = 1.0
    else:
        s = (c * t)
    return (c, s)