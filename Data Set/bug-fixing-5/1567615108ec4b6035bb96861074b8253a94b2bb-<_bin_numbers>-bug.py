def _bin_numbers(sample, nbin, edges, dedges):
    'Compute the bin number each sample falls into, in each dimension\n    '
    (Dlen, Ndim) = sample.shape
    sampBin = [np.digitize(sample[:, i], edges[i]) for i in xrange(Ndim)]
    exceptions = (RuntimeWarning,)
    if (sys.version_info >= (3, 8)):
        exceptions += (OverflowError,)
    for i in xrange(Ndim):
        try:
            decimal = (int((- np.log10(dedges[i].min()))) + 6)
        except exceptions:
            raise ValueError('The smallest edge difference is numerically 0.')
        on_edge = np.where((np.around(sample[:, i], decimal) == np.around(edges[i][(- 1)], decimal)))[0]
        sampBin[i][on_edge] -= 1
    binnumbers = np.ravel_multi_index(sampBin, nbin)
    return binnumbers