def test_pycuda_memory_to_theano():
    y = pycuda.gpuarray.zeros((3, 4, 5), 'float32')
    print(sys.getrefcount(y))
    initial_refcount = sys.getrefcount(y)
    print('gpuarray ref count before creating a CudaNdarray', end=' ')
    print(sys.getrefcount(y))
    assert (sys.getrefcount(y) == initial_refcount)
    rand = numpy.random.randn(*y.shape).astype(numpy.float32)
    cuda_rand = cuda_ndarray.CudaNdarray(rand)
    strides = [1]
    for i in y.shape[::(- 1)][:(- 1)]:
        strides.append((strides[(- 1)] * i))
    strides = tuple(strides[::(- 1)])
    print('strides', strides)
    assert (cuda_rand._strides == strides), (cuda_rand._strides, strides)
    y_ptr = int(y.gpudata)
    z = cuda_ndarray.from_gpu_pointer(y_ptr, y.shape, strides, y)
    print('gpuarray ref count after creating a CudaNdarray', sys.getrefcount(y))
    assert (sys.getrefcount(y) == (initial_refcount + 1))
    assert (numpy.asarray(z) == 0).all()
    assert (z.base is y)
    zz = z.view()
    assert (sys.getrefcount(y) == (initial_refcount + 2))
    assert (zz.base is y)
    del zz
    assert (sys.getrefcount(y) == (initial_refcount + 1))
    cuda_ones = cuda_ndarray.CudaNdarray(numpy.asarray([[[1]]], dtype='float32'))
    z += cuda_ones
    assert (numpy.asarray(z) == numpy.ones(y.shape)).all()
    assert (numpy.asarray(z) == 1).all()
    assert (cuda_rand.shape == z.shape)
    assert (cuda_rand._strides == z._strides), (cuda_rand._strides, z._strides)
    assert (numpy.asarray(cuda_rand) == rand).all()
    z += cuda_rand
    assert (numpy.asarray(z) == (rand + 1)).all()
    del z
    print('gpuarray ref count after deleting the CudaNdarray', end=' ')
    print(sys.getrefcount(y))
    assert (sys.getrefcount(y) == initial_refcount)