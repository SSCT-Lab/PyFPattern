@with_seed()
def test_deformable_convolution_with_type():
    tol = {
        np.dtype(np.float32): 0.1,
        np.dtype(np.float64): 0.001,
    }
    sym = mx.sym.contrib.DeformableConvolution(num_filter=3, kernel=(3, 3), name='deformable_conv')
    ctx_list = [{
        'ctx': mx.gpu(0),
        'deformable_conv_data': (2, 2, 10, 10),
        'deformable_conv_offset': (2, 18, 8, 8),
        'type_dict': {
            'deformable_conv_data': np.float64,
            'deformable_conv_offset': np.float64,
        },
    }, {
        'ctx': mx.gpu(0),
        'deformable_conv_data': (2, 2, 10, 10),
        'deformable_conv_offset': (2, 18, 8, 8),
        'type_dict': {
            'deformable_conv_data': np.float32,
            'deformable_conv_offset': np.float32,
        },
    }]
    check_consistency(sym, ctx_list, scale=0.1, tol=tol)
    check_consistency(sym, ctx_list, scale=0.1, tol=tol, grad_req={
        'deformable_conv_data': 'write',
        'deformable_conv_offset': 'write',
        'deformable_conv_weight': 'write',
        'deformable_conv_bias': 'null',
    })