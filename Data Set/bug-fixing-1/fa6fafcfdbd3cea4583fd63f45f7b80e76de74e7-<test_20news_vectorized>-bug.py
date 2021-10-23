

def test_20news_vectorized():
    raise SkipTest('Test too slow.')
    bunch = datasets.fetch_20newsgroups_vectorized(subset='train')
    assert_true(sp.isspmatrix_csr(bunch.data))
    assert_equal(bunch.data.shape, (11314, 107428))
    assert_equal(bunch.target.shape[0], 11314)
    assert_equal(bunch.data.dtype, np.float64)
    bunch = datasets.fetch_20newsgroups_vectorized(subset='test')
    assert_true(sp.isspmatrix_csr(bunch.data))
    assert_equal(bunch.data.shape, (7532, 107428))
    assert_equal(bunch.target.shape[0], 7532)
    assert_equal(bunch.data.dtype, np.float64)
    bunch = datasets.fetch_20newsgroups_vectorized(subset='all')
    assert_true(sp.isspmatrix_csr(bunch.data))
    assert_equal(bunch.data.shape, ((11314 + 7532), 107428))
    assert_equal(bunch.target.shape[0], (11314 + 7532))
    assert_equal(bunch.data.dtype, np.float64)
