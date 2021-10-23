def check_fft(shape):
    sym = mx.sym.contrib.fft(name='fft', compute_size=128)
    if (len(shape) == 2):
        if ((shape[1] % 2) != 0):
            lst = list(shape)
            lst[1] = (lst[1] * 2)
            shape = tuple(lst)
            shape_old = shape
    if (len(shape) == 4):
        if ((shape[3] % 2) != 0):
            lst = list(shape)
            lst[3] = (lst[3] * 2)
            shape = tuple(lst)
            shape_old = shape
    init = [np.random.normal(size=shape, scale=1.0)]
    arr_grad = [mx.nd.empty(shape)]
    ctx_list = [{
        'ctx': mx.gpu(0),
        'fft_data': shape,
        'type_dict': {
            'fft_data': np.float32,
        },
    }]
    exe_list = [sym.simple_bind(args_grad=arr_grad, **ctx) for ctx in ctx_list]
    for exe in exe_list:
        for (arr, iarr) in zip(exe.arg_arrays, init):
            arr[:] = iarr.astype(arr.dtype)
    for exe in exe_list:
        exe.forward(is_train=True)
    out1 = [exe.outputs[0].asnumpy() for exe in exe_list]
    out = np.fft.fft(init, n=None, axis=(- 1), norm=None)
    if (len(shape) == 2):
        out = np.reshape(out, (out.shape[1], out.shape[2]))
        out2 = np.append(out.real, out.imag, axis=1)
        a = np.zeros(out1[0].shape)
        p = 0
        for i in range((out2.shape[1] // 2)):
            a[:, p] = out2[:, i]
            a[:, (p + 1)] = out2[:, (i + (out2.shape[1] // 2))]
            p = (p + 2)
    if (len(shape) == 4):
        out = np.reshape(out, (out.shape[1], out.shape[2], out.shape[3], out.shape[4]))
        out2 = np.append(out.real, out.imag, axis=1)
        a = np.zeros(out1[0].shape)
        for i in range(out1[0].shape[0]):
            for j in range(out1[0].shape[1]):
                p = 0
                for k in range(out2.shape[3]):
                    a[i, j, :, p] = out2[i, j, :, k]
                    a[i, j, :, (p + 1)] = out2[i, (j + out1[0].shape[1]), :, k]
                    p = (p + 2)
    assert_almost_equal(a, out1[0], rtol=0.001, atol=1e-06)
    if (len(shape) == 2):
        out_grad = mx.nd.empty((shape[0], (2 * shape[1])))
        out_grad[:] = np.random.normal((- 3), 3, (shape[0], (2 * shape[1])))
        out_grad_complex = np.zeros(shape, dtype=np.complex64)
        for i in range(0, shape[1]):
            out_grad_complex.real[:, i] = out_grad.asnumpy()[:, (2 * i)]
            out_grad_complex.imag[:, i] = out_grad.asnumpy()[:, ((2 * i) + 1)]
        for exe in exe_list:
            exe.backward([out_grad])
        a = np.fft.ifft(out_grad_complex, n=None, axis=(- 1), norm=None)
        assert_almost_equal(a.real, (exe.grad_arrays[0].asnumpy() / shape[1]), rtol=0.001, atol=1e-08)
    if (len(shape) == 4):
        out_grad = mx.nd.empty(out1[0].shape)
        out_grad[:] = np.random.normal((- 3), 3, out1[0].shape)
        out_grad_complex = np.zeros(shape, dtype=np.complex64)
        for i in range(0, shape[3]):
            out_grad_complex.real[:, :, :, i] = out_grad.asnumpy()[:, :, :, (2 * i)]
            out_grad_complex.imag[:, :, :, i] = out_grad.asnumpy()[:, :, :, ((2 * i) + 1)]
        for exe in exe_list:
            exe.backward([out_grad])
        a = np.fft.ifft(out_grad_complex, n=None, axis=(- 1), norm=None)
        assert_almost_equal(a.real, (exe.grad_arrays[0].asnumpy() / shape[3]), rtol=0.001, atol=1e-06)