def check_ifft(shape):
    shape_old = shape
    if (len(shape) == 2):
        if ((shape[1] % 2) != 0):
            lst = list(shape)
            lst[1] = (lst[1] * 2)
            shape = tuple(lst)
            shape_old = shape
        shape = (shape[0], (shape[1] * 2))
    if (len(shape) == 4):
        if ((shape[3] % 2) != 0):
            lst = list(shape)
            lst[3] = (lst[3] * 2)
            shape = tuple(lst)
            shape_old = shape
        shape = (shape[0], shape[1], shape[2], (shape[3] * 2))
    sym = mx.sym.contrib.ifft(name='ifft', compute_size=128)
    init = [np.random.normal(size=shape, scale=1.0)]
    arr_grad = [mx.nd.empty(shape)]
    ctx_list = [{
        'ctx': mx.gpu(0),
        'ifft_data': shape,
        'type_dict': {
            'ifft_data': np.float32,
        },
    }]
    exe_list = [sym.simple_bind(args_grad=arr_grad, **ctx) for ctx in ctx_list]
    for exe in exe_list:
        for (arr, iarr) in zip(exe.arg_arrays, init):
            arr[:] = iarr.astype(arr.dtype)
    for exe in exe_list:
        exe.forward(is_train=True)
        out1 = [exe.outputs[0].asnumpy() for exe in exe_list]
    if (len(shape) == 2):
        init_complex = np.zeros(shape_old, dtype=np.complex64)
        for i in range(0, shape_old[1]):
            init_complex.real[:, i] = init[0][:, (2 * i)]
            init_complex.imag[:, i] = init[0][:, ((2 * i) + 1)]
        a = np.fft.ifft(init_complex, n=None, axis=(- 1), norm=None)
        assert_almost_equal(a.real, (out1[0] / shape_old[1]), rtol=0.001, atol=1e-05)
    if (len(shape) == 4):
        init_complex = np.zeros(shape_old, dtype=np.complex64)
        for i in range(0, shape_old[3]):
            init_complex.real[:, :, :, i] = init[0][:, :, :, (2 * i)]
            init_complex.imag[:, :, :, i] = init[0][:, :, :, ((2 * i) + 1)]
        a = np.fft.ifft(init_complex, n=None, axis=(- 1), norm=None)
        assert_almost_equal(a.real, (out1[0] / shape_old[3]), rtol=0.001, atol=1e-05)
    if (len(shape) == 2):
        out_grad = mx.nd.empty(shape_old)
        out_grad[:] = np.random.normal((- 3), 3, shape_old)
        for exe in exe_list:
            exe.backward([out_grad])
            temp = exe.grad_arrays[0].asnumpy()
            temp = np.zeros(shape_old)
            for i in range(shape_old[1]):
                temp[:, i] = exe.grad_arrays[0].asnumpy()[:, (2 * i)]
        a = np.fft.fft(out_grad.asnumpy(), n=None, axis=(- 1), norm=None)
        assert_almost_equal(a.real, temp, rtol=0.001, atol=1e-05)
    if (len(shape) == 4):
        out_grad = mx.nd.empty(shape_old)
        out_grad[:] = np.random.normal((- 3), 3, shape_old)
        for exe in exe_list:
            exe.backward([out_grad])
            temp = exe.grad_arrays[0].asnumpy()
            temp = np.zeros(shape_old)
            for i in range(shape_old[3]):
                temp[:, :, :, i] = exe.grad_arrays[0].asnumpy()[:, :, :, (2 * i)]
        a = np.fft.fft(out_grad.asnumpy(), n=None, axis=(- 1), norm=None)
        assert_almost_equal(a.real, temp, rtol=0.001, atol=1e-05)