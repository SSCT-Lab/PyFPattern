def sequence_pool(input, pool_type, **kwargs):
    ENUM_POOL_TYPE = set(['MAX', 'AVG', 'SQRT', 'LAST', 'FIRST'])
    if (pool_type.upper() not in ENUM_POOL_TYPE):
        raise ValueError("Unknown pool_type: '%s'. It can only be %s.", str(pool_type), ' '.join(ENUM_POOL_TYPE))
    helper = LayerHelper('sequence_pool', input=input, **kwargs)
    dtype = helper.input_dtype()
    pool_out = helper.create_tmp_variable(dtype)
    helper.append_op(type='sequence_pool', inputs={
        'X': [input],
    }, outputs={
        'Out': [pool_out],
    }, attrs={
        'pooltype': pool_type.upper(),
    })
    return pool_out