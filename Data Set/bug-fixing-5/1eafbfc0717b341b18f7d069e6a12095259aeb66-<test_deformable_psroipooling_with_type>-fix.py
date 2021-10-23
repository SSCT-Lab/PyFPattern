@with_seed()
def test_deformable_psroipooling_with_type():
    tol = {
        np.dtype(np.float32): 0.1,
        np.dtype(np.float64): 0.001,
        np.dtype(np.float16): 0.01,
    }
    arg_params = {
        'deformable_psroipool_rois': np.array([[0, 10, 22, 161, 173], [0, 20, 15, 154, 160]]),
    }
    sym = mx.sym.contrib.DeformablePSROIPooling(spatial_scale=0.0625, sample_per_part=4, group_size=3, pooled_size=3, output_dim=2, trans_std=0.1, no_trans=False, name='deformable_psroipool')
    ctx_list = [{
        'ctx': mx.gpu(0),
        'deformable_psroipool_data': (1, 18, 14, 14),
        'deformable_psroipool_rois': (2, 5),
        'deformable_psroipool_trans': (2, 4, 3, 3),
        'type_dict': {
            'deformable_psroipool_data': np.float64,
            'deformable_psroipool_rois': np.float64,
            'deformable_psroipool_trans': np.float64,
        },
    }, {
        'ctx': mx.gpu(0),
        'deformable_psroipool_data': (1, 18, 14, 14),
        'deformable_psroipool_rois': (2, 5),
        'deformable_psroipool_trans': (2, 4, 3, 3),
        'type_dict': {
            'deformable_psroipool_data': np.float32,
            'deformable_psroipool_rois': np.float32,
            'deformable_psroipool_trans': np.float32,
        },
    }, {
        'ctx': mx.gpu(0),
        'deformable_psroipool_data': (1, 18, 14, 14),
        'deformable_psroipool_rois': (2, 5),
        'deformable_psroipool_trans': (2, 4, 3, 3),
        'type_dict': {
            'deformable_psroipool_data': np.float16,
            'deformable_psroipool_rois': np.float16,
            'deformable_psroipool_trans': np.float16,
        },
    }]
    check_consistency(sym, ctx_list, scale=0.1, tol=tol, grad_req={
        'deformable_psroipool_data': 'write',
        'deformable_psroipool_rois': 'null',
        'deformable_psroipool_trans': 'write',
    }, arg_params=arg_params)