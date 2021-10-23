def _bin_numbers(sample, nbin, edges, dedges):
    'Compute the bin number each sample falls into, in each dimension\n    '
    (Dlen, Ndim) = sample.shape
    sampBin = [np.digitize(sample[:, i], edges[i]) for i in xrange(Ndim)]
    for i in xrange(Ndim):
        dedges_min = dedges[i].min()
        if (dedges_min == 0):
            raise ValueError('The smallest edge difference is numerically 0.')
        decimal = (int((- np.log10(dedges_min))) + 6)
        on_edge = np.where((np.around(sample[:, i], decimal) == np.around(edges[i][(- 1)], decimal)))[0]
        sampBin[i][on_edge] -= 1
    binnumbers = np.ravel_multi_index(sampBin, nbin)
    return binnumbers