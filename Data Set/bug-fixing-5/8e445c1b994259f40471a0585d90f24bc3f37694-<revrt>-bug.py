def revrt(X, m=None):
    '\n    Inverse of forrt. Equivalent to Munro (1976) REVRT routine.\n    '
    if (m is None):
        m = len(X)
    y = (X[:((m // 2) + 1)] + (np.r_[(0, X[((m // 2) + 1):], 0)] * 1j))
    return (np.fft.irfft(y) * m)