

@templatedoc()
def strided_slice(input, axes, starts, ends, strides):
    '\n    This operator produces a slice of ``input`` along multiple axes. Similar to numpy:\n    https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html\n    Slice uses ``axes``, ``starts`` and ``ends`` attributes to specify the start and\n    end dimension for each axis in the list of axes and Slice uses this information\n    to slice the input data tensor. If a negative value is passed to\n    ``starts`` or ``ends`` such as :math:`-i`,  it represents the reverse position of the\n    axis :math:`i-1` th(here 0 is the initial position). The ``strides`` represents steps of\n    slicing and if the ``strides`` is negative, slice operation is in the opposite direction.\n    If the value passed to ``starts`` or ``ends`` is greater than n\n    (the number of elements in this dimension), it represents n.\n    For slicing to the end of a dimension with unknown size, it is recommended\n    to pass in INT_MAX. The size of ``axes`` must be equal to ``starts`` , ``ends`` and ``strides``.\n    Following examples will explain how strided_slice works:\n\n    .. code-block:: text\n\n        Case1:\n            Given:\n                data = [ [1, 2, 3, 4], [5, 6, 7, 8], ]\n                axes = [0, 1]\n                starts = [1, 0]\n                ends = [2, 3]\n                strides = [1, 1]\n            Then:\n                result = [ [5, 6, 7], ]\n        \n        Case2:\n            Given:\n                data = [ [1, 2, 3, 4], [5, 6, 7, 8], ]\n                axes = [0, 1]\n                starts = [0, 1]\n                ends = [2, 0]\n                strides = [1, -1]\n            Then:\n                result = [ [8, 7, 6], ]\n        \n        Case3:\n            Given:\n                data = [ [1, 2, 3, 4], [5, 6, 7, 8], ]\n                axes = [0, 1]\n                starts = [-1, 1000]\n                ends = [-1, 1000]\n                strides = [1, 3]\n            Then:\n                result = [ [2], ]\n    Args:\n        input (Variable): An N-D ``Tensor`` or ``LoDTensor`` . The data type is ``float32``, ``float64``, ``int32`` or ``int64``.\n        axes (list|tuple): The data type is ``int32`` . Axes that `starts` and `ends` apply to.\n                            It\'s optional. If it is not provides, it will be treated as :math:`[0,1,...,len(starts)-1]`.\n        starts (list|tuple|Variable): The data type is ``int32`` . If ``starts`` is a list or tuple, the elements of\n                it should be integers or Tensors with shape [1]. If ``starts`` is an Variable, it should be an 1-D Tensor.\n                It represents starting indices of corresponding axis in ``axes``.\n        ends (list|tuple|Variable): The data type is ``int32`` . If ``ends`` is a list or tuple, the elements of\n                it should be integers or Tensors with shape [1]. If ``ends`` is an Variable, it should be an 1-D Tensor .\n                It represents ending indices of corresponding axis in ``axes``.\n        strides (list|tuple|Variable): The data type is ``int32`` . If ``strides`` is a list or tuple, the elements of\n                it should be integers or Tensors with shape [1]. If ``strides`` is an Variable, it should be an 1-D Tensor .\n                It represents slice step of corresponding axis in ``axes``.\n\n    Returns:\n        Variable:  A ``Tensor`` or ``LoDTensor`` with the same dimension as ``input``. The data type is same as ``input``.\n\n    Raises:\n        TypeError: The type of ``starts`` must be list, tuple or Variable.\n        TypeError: The type of ``ends`` must be list, tuple or Variable.\n        TypeError: The type of ``strides`` must be list, tuple or Variable.\n\n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n\n            input = fluid.data(\n                name="input", shape=[3, 4, 5, 6], dtype=\'float32\')\n\n            # example 1:\n            # attr starts is a list which doesn\'t contain tensor Variable.\n            axes = [0, 1, 2]\n            starts = [-3, 0, 2]\n            ends = [3, 2, 4]\n            strides_1 = [1, 1, 1]\n            strides_2 = [1, 1, 2]\n            sliced_1 = fluid.layers.strided_slice(input, axes=axes, starts=starts, ends=ends, strides=strides_1)\n            # sliced_1 is input[:, 0:3:1, 0:2:1, 2:4:1].\n\n\n            # example 2:\n            # attr starts is a list which contain tensor Variable.\n            minus_3 = fluid.layers.fill_constant([1], "int32", -3)\n            sliced_2 = fluid.layers.strided_slice(input, axes=axes, starts=[minus_3, 0, 2], ends=ends, strides=strides_2)\n            # sliced_2 is input[:, 0:3:1, 0:2:1, 2:4:2].\n    '
    if (not isinstance(starts, (list, tuple, Variable))):
        raise ValueError('Input starts must be an Variable, python list or tuple.')
    if (not isinstance(ends, (list, tuple, Variable))):
        raise ValueError('Input ends must be an Variable, python list or tuple.')
    if (not isinstance(strides, (list, tuple, Variable))):
        raise ValueError('Input strides must be an Variable, python list or tuple.')
    helper = LayerHelper('strided_slice', **locals())

    def contain_var(one_list):
        for ele in one_list:
            if isinstance(ele, Variable):
                return True
        return False

    def get_new_list_tensor(old_list):
        new_list_tensor = []
        for dim in old_list:
            if isinstance(dim, Variable):
                dim.stop_gradient = True
                new_list_tensor.append(dim)
            else:
                assert isinstance(dim, int)
                temp_out = helper.create_variable_for_type_inference('int32')
                fill_constant([1], 'int32', dim, force_cpu=True, out=temp_out)
                new_list_tensor.append(temp_out)
        return new_list_tensor
    inputs = {
        'Input': input,
    }
    attrs = {
        'axes': axes,
    }
    infer_flags = list((1 for i in range(len(axes))))
    if in_dygraph_mode():
        inputs = {
            'Input': input,
        }
        attrs = {
            'axes': axes,
            'starts': starts,
            'ends': ends,
            'strides': strides,
            'infer_flags': infer_flags,
        }
    else:
        if isinstance(starts, Variable):
            starts.stop_gradient = True
            inputs['StartsTensor'] = starts
        elif isinstance(starts, (list, tuple)):
            attrs['starts'] = []
            if (not contain_var(starts)):
                attrs['starts'] = starts
            else:
                inputs['StartsTensorList'] = get_new_list_tensor(starts)
                for (i, dim) in enumerate(starts):
                    if isinstance(dim, Variable):
                        attrs['starts'].append((- 1))
                        infer_flags[i] = (- 1)
                    else:
                        attrs['starts'].append(dim)
        if isinstance(ends, Variable):
            ends.stop_gradient = True
            inputs['EndsTensor'] = ends
        elif isinstance(ends, (list, tuple)):
            attrs['ends'] = []
            if (not contain_var(ends)):
                attrs['ends'] = ends
            else:
                inputs['EndsTensorList'] = get_new_list_tensor(ends)
                for (i, dim) in enumerate(ends):
                    if isinstance(dim, Variable):
                        attrs['ends'].append((- 1))
                        infer_flags[i] = (- 1)
                    else:
                        attrs['ends'].append(dim)
        if isinstance(strides, Variable):
            strides.stop_gradient = True
            inputs['StridesTensor'] = strides
        elif isinstance(strides, (list, tuple)):
            attrs['strides'] = []
            if (not contain_var(strides)):
                attrs['strides'] = strides
            else:
                inputs['StridesTensorList'] = get_new_list_tensor(strides)
                for (i, dim) in enumerate(strides):
                    if isinstance(dim, Variable):
                        attrs['strides'].append((- 1))
                        infer_flags[i] = (- 1)
                    else:
                        attrs['strides'].append(dim)
        attrs['infer_flags'] = infer_flags
    out = helper.create_variable_for_type_inference(dtype=helper.input_dtype('input'))
    helper.append_op(type='strided_slice', inputs=inputs, attrs=attrs, outputs={
        'Out': out,
    })
    return out
