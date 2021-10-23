def test_aligned_mem_float():
    'Check linalg works with non-aligned memory (float32)'
    a = arange(402, dtype=np.uint8)
    z = np.frombuffer(a.data, offset=2, count=100, dtype=float32)
    z.shape = (10, 10)
    eig(z, overwrite_a=True)
    eig(z.T, overwrite_a=True)