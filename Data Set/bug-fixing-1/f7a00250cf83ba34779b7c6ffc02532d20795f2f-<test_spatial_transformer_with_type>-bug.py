

@unittest.skip('test fails intermittently. temporarily disabled till it gets fixed. tracked at https://github.com/apache/incubator-mxnet/issues/7645')
@with_seed(1234)
def test_spatial_transformer_with_type():
    data = mx.sym.Variable('data')
    loc = mx.sym.Flatten(data)
    loc = mx.sym.FullyConnected(data=loc, num_hidden=10)
    loc = mx.sym.Activation(data=loc, act_type='relu')
    loc = mx.sym.FullyConnected(data=loc, num_hidden=6)
    sym = mx.sym.SpatialTransformer(data=data, loc=loc, target_shape=(10, 10), transform_type='affine', sampler_type='bilinear')
    ctx_list = [{
        'ctx': mx.gpu(0),
        'data': (1, 5, 10, 10),
        'type_dict': {
            'data': np.float32,
        },
    }, {
        'ctx': mx.cpu(0),
        'data': (1, 5, 10, 10),
        'type_dict': {
            'data': np.float32,
        },
    }]
    check_consistency(sym, ctx_list)
    check_consistency(sym, ctx_list, grad_req='add')
