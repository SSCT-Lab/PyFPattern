@templatedoc()
def random_crop(x, shape, seed=None):
    '\n    ${comment}\n\n    Examples:\n        >>> img = fluid.layers.data("img", [3, 256, 256])\n        >>> cropped_img = fluid.layers.random_crop(img, shape=[3, 224, 224])\n\n    Args:\n        x(${x_type}): ${x_comment}\n        shape(${shape_type}): ${shape_comment}\n        seed(int|${seed_type}|None): ${seed_comment} By default, the seed will\n            get from `random.randint(-65536, 65535)`.\n\n    Returns:\n        ${out_comment}\n\n    '
    helper = LayerHelper('random_crop', **locals())
    dtype = helper.input_dtype()
    out = helper.create_tmp_variable(dtype)
    if (seed is None):
        seed = random.randint((- 65536), 65535)
    if isinstance(seed, int):
        seed_value = seed
        seed = helper.create_tmp_variable(dtype='int64')
        helper.append_op(type='fill_constant', inputs={
            
        }, outputs={
            'Out': seed,
        }, attrs={
            'dtype': seed.dtype,
            'shape': [1],
            'value': float(seed_value),
            'force_cpu': True,
        })
    elif (not isinstance(seed, Variable)):
        raise ValueError("'seed' must be a Variable or an int.")
    seed_out = helper.create_tmp_variable(dtype='int64')
    helper.append_op(type='random_crop', inputs={
        'X': input,
        'Seed': seed,
    }, outputs={
        'Out': out,
        'SeedOut': seed_out,
    }, attrs={
        'shape': shape,
    })
    return out