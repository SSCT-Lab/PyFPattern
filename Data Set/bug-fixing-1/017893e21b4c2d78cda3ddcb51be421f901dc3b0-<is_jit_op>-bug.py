

def is_jit_op(decl):
    return ((not decl['api_name'].endswith('_')) and (not decl['name'].endswith('_out')) and (not decl['name'].endswith('_forward')) and (not any(((arg['simple_type'] == 'Generator') for arg in decl['arguments']))) and (not any(((arg['simple_type'] == 'SparseTensor') for arg in decl['arguments']))) and (not any(((arg['simple_type'] == 'Storage') for arg in decl['arguments']))) and any(((arg['simple_type'] in {'Tensor', 'TensorList'}) for arg in decl['arguments'])) and ('Tensor' in decl['return_type']))
