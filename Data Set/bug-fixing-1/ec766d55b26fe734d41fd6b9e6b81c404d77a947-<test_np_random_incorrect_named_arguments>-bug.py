

@with_seed()
@use_np
def test_np_random_incorrect_named_arguments():
    random_ops = ['uniform', 'normal', 'randint']
    for op_name in random_ops:
        op = getattr(mx.np.random, op_name, None)
        assert (op is not None)
        assert_raises(TypeError, op, shape=())
        assert_raises(TypeError, op, shape=None)
