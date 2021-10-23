def _norm_pdf(x):
    return (np.exp(((- (x ** 2)) / 2.0)) / _norm_pdf_C)