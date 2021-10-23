@pytest.mark.skip((platform.machine() == 'ppc64le'), reason='crashes on ppc64le')
def test_aligned_mem():
    'Check linalg works with non-aligned memory (float64)'
    a = arange(804, dtype=np.uint8)
    z = np.frombuffer(a.data, offset=4, count=100, dtype=float)
    z.shape = (10, 10)
    eig(z, overwrite_a=True)
    eig(z.T, overwrite_a=True)