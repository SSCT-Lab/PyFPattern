@with_seed()
def test_sparse_nd_pickle():
    dim0 = 40
    dim1 = 40
    stypes = ['row_sparse', 'csr']
    densities = [0, 0.5]
    stype_dict = {
        'row_sparse': RowSparseNDArray,
        'csr': CSRNDArray,
    }
    shape = rand_shape_2d(dim0, dim1)
    for stype in stypes:
        for density in densities:
            (a, _) = rand_sparse_ndarray(shape, stype, density)
            assert isinstance(a, stype_dict[stype])
            data = pkl.dumps(a)
            b = pkl.loads(data)
            assert isinstance(b, stype_dict[stype])
            assert same(a.asnumpy(), b.asnumpy())