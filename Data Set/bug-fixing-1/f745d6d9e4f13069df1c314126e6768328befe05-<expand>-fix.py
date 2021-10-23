

def expand(x, expand_times, name=None):
    "Expand operator tiles the input by given times number. You should set times\n    number for each dimension by providing attribute 'expand_times'. The rank of X\n    should be in [1, 6]. Please note that size of 'expand_times' must be the same\n    with X's rank. Following is a using case:\n\n\n    .. code-block:: text\n\n        Input(X) is a 3-D tensor with shape [2, 3, 1]:\n\n                [\n                   [[1], [2], [3]],\n                   [[4], [5], [6]]\n                ]\n\n        Attr(expand_times):  [1, 2, 2]\n\n        Output(Out) is a 3-D tensor with shape [2, 6, 2]:\n\n                [\n                    [[1, 1], [2, 2], [3, 3], [1, 1], [2, 2], [3, 3]],\n                    [[4, 4], [5, 5], [6, 6], [4, 4], [5, 5], [6, 6]]\n                ]\n\n    Args:\n        x (Variable): A tensor with rank in [1, 6].\n        expand_times (list|tuple): Expand times number for each dimension.\n\n    Returns:\n        Variable: The expanded variable which is a LoDTensor. After expanding, size of each dimension of Output(Out) is equal to ithe size of the corresponding dimension of Input(X) multiplying the corresponding value given by expand_times.\n\n\n    Examples:\n        .. code-block:: python\n          \n            import paddle.fluid as fluid\n            x = fluid.layers.fill_constant(shape=[2, 3, 1], dtype='int32', value=0)\n            out = fluid.layers.expand(x=x, expand_times=[1, 2, 2])\n    "
    helper = LayerHelper('expand', input=x, **locals())
    dtype = helper.input_dtype(input_param_name='x')
    out = helper.create_variable_for_type_inference(dtype)
    if in_dygraph_mode():
        inputs = {
            'X': x,
        }
        attrs = {
            'expand_times': expand_times,
        }
    else:

        def contain_tensor(expand_times):
            for ele in expand_times:
                if isinstance(ele, Variable):
                    return True
            return False
        if contain_tensor(expand_times):
            new_expand_times = []
            for ele in expand_times:
                if isinstance(ele, Variable):
                    ele.stop_gradient = True
                    new_expand_times.append(ele)
                else:
                    assert isinstance(ele, int)
                    temp_out = helper.create_variable_for_type_inference('int32')
                    fill_constant([1], 'int32', ele, force_cpu=True, out=temp_out)
                    new_expand_times.append(temp_out)
            inputs = {
                'X': x,
                'expand_times_tensor': new_expand_times,
            }
            attrs = {
                
            }
        else:
            inputs = {
                'X': x,
            }
            attrs = {
                'expand_times': expand_times,
            }
    helper.append_op(type='expand', inputs=inputs, outputs={
        'Out': out,
    }, attrs=attrs)
    return out
