def revrt(X, m=None):
    '\n    Inverse of forrt. Equivalent to Munro (1976) REVRT routine.\n    '
    if (m is None):
        m = len(X)
    i = int(((m // 2) + 1))
    y = (X[:i] + (np.r_[(0, X[i:], 0)] * 1j))
    return (np.fft.irfft(y) * m)