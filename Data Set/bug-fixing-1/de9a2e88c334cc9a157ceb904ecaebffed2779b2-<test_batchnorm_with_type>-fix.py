

@with_seed()
def test_batchnorm_with_type():
    ctx_list_v1_2D = [{
        'ctx': mx.cpu(0),
        'norm_data': (10, 2, 10, 10),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (10, 2, 10, 10),
        'type_dict': {
            'norm_data': np.float32,
        },
    }]
    ctx_list_v2_2D = [{
        'ctx': mx.cpu(0),
        'norm_data': (5, 2, 5, 5),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.cpu(0),
        'norm_data': (5, 2, 5, 5),
        'type_dict': {
            'norm_data': np.float16,
        },
    }, {
        'ctx': mx.cpu(0),
        'norm_data': (5, 2, 5, 5),
        'type_dict': {
            'norm_data': np.float64,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (5, 2, 5, 5),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (5, 2, 5, 5),
        'type_dict': {
            'norm_data': np.float16,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (5, 2, 5, 5),
        'type_dict': {
            'norm_data': np.float64,
        },
    }]
    ctx_list_v2_1D = [{
        'ctx': mx.cpu(0),
        'norm_data': (5, 2, 5),
        'type_dict': {
            'norm_data': np.float16,
        },
    }, {
        'ctx': mx.cpu(0),
        'norm_data': (5, 2, 5),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.cpu(0),
        'norm_data': (5, 2, 5),
        'type_dict': {
            'norm_data': np.float64,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (5, 2, 5),
        'type_dict': {
            'norm_data': np.float16,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (5, 2, 5),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (5, 2, 5),
        'type_dict': {
            'norm_data': np.float64,
        },
    }]
    ctx_list_v2_3D = [{
        'ctx': mx.cpu(0),
        'norm_data': (3, 2, 3, 2, 3),
        'type_dict': {
            'norm_data': np.float16,
        },
    }, {
        'ctx': mx.cpu(0),
        'norm_data': (3, 2, 3, 2, 3),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.cpu(0),
        'norm_data': (3, 2, 3, 2, 3),
        'type_dict': {
            'norm_data': np.float64,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (3, 2, 3, 2, 3),
        'type_dict': {
            'norm_data': np.float16,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (3, 2, 3, 2, 3),
        'type_dict': {
            'norm_data': np.float32,
        },
    }, {
        'ctx': mx.gpu(0),
        'norm_data': (3, 2, 3, 2, 3),
        'type_dict': {
            'norm_data': np.float64,
        },
    }]
    sym = mx.sym.BatchNorm_v1(name='norm', fix_gamma=False)
    check_consistency(sym, ctx_list_v1_2D)
    sym = mx.sym.BatchNorm_v1(name='norm', fix_gamma=True)
    check_consistency(sym, ctx_list_v1_2D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=False, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_2D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=False, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_2D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=True, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_2D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=True, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_2D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=False, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_1D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=False, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_1D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=True, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_1D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=True, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_1D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=False, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_3D)
    sym = mx.sym.BatchNorm(name='norm', fix_gamma=True, cudnn_off=True)
    check_consistency(sym, ctx_list_v2_3D)
