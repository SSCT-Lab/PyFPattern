@with_seed()
def test_update_ops_mutation():

    def assert_mutate(x, y, op):
        np.testing.assert_raises(AssertionError, np.testing.assert_allclose, x, y)

    def assert_unchanged(x, y, op):
        np.testing.assert_allclose(x, y)

    def test_op(op, num_inputs, mutated_inputs, **kwargs):
        for dim in range(1, 7):
            shape = rand_shape_nd(dim)
            shapes = ((shape,) * num_inputs)
            arrays = tuple(map(mx.nd.array, random_arrays(*shapes)))
            pre_arrays = tuple(map((lambda x: x.asnumpy()), arrays))
            op(*arrays, out=arrays[0], **kwargs)
            post_arrays = tuple(map((lambda x: x.asnumpy()), arrays))
            for (idx, (pre_array, post_array)) in enumerate(zip(pre_arrays, post_arrays)):
                if (idx in mutated_inputs):
                    assert_mutate(pre_array, post_array, op)
                else:
                    assert_unchanged(pre_array, post_array, op)
    test_op(mx.nd.signsgd_update, 2, [0], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
        'clip_gradient': 0.001,
    })
    test_op(mx.nd.signum_update, 3, [0, 2], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
        'momentum': 0.001,
        'clip_gradient': 0.001,
        'wd_lh': 0.001,
    })
    test_op(mx.nd.sgd_update, 2, [0], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
        'clip_gradient': 0.001,
    })
    test_op(mx.nd.sgd_mom_update, 3, [0, 2], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
        'momentum': 0.01,
        'clip_gradient': 0.001,
    })
    test_op(mx.nd.nag_mom_update, 3, [0, 2], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
        'momentum': 0.01,
        'clip_gradient': 0.001,
    })
    test_op(mx.nd.ftml_update, 5, [0, 2, 3, 4], **{
        't': 3,
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
        'clip_grad': 0.001,
    })
    test_op(mx.nd.ftrl_update, 4, [0, 2, 3], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
    })
    test_op(mx.nd.adam_update, 4, [0, 2, 3], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
    })
    test_op(mx.nd.rmspropalex_update, 5, [0, 2, 3, 4], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
    })
    test_op(mx.nd.rmsprop_update, 3, [0, 2], **{
        'rescale_grad': 0.1,
        'lr': 0.01,
        'wd': 0.001,
    })