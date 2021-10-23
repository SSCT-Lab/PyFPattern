def _pdf_skip(self, x, dfn, dfd, nc):
    (n1, n2) = (dfn, dfd)
    term = (((((- nc) / 2) + (((nc * n1) * x) / (2 * (n2 + (n1 * x))))) + sc.gammaln((n1 / 2.0))) + sc.gammaln((1 + (n2 / 2.0))))
    term -= sc.gammaln(((n1 + n2) / 2.0))
    Px = np.exp(term)
    Px *= (((n1 ** (n1 / 2)) * (n2 ** (n2 / 2))) * (x ** ((n1 / 2) - 1)))
    Px *= ((n2 + (n1 * x)) ** ((- (n1 + n2)) / 2))
    Px *= sc.assoc_laguerre(((((- nc) * n1) * x) / (2.0 * (n2 + (n1 * x)))), (n2 / 2), ((n1 / 2) - 1))
    Px /= sc.beta((n1 / 2), (n2 / 2))