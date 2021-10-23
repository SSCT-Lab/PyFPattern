def _arguments_validation(self, layers, mode, concat_axis, dot_axes, node_indices, tensor_indices):
    'Validates user-passed arguments and raises exceptions\n        as appropriate.\n        '
    if (not hasattr(mode, '__call__')):
        if (mode not in {'sum', 'mul', 'concat', 'ave', 'cos', 'dot'}):
            raise Exception(('Invalid merge mode: ' + str(mode)))
    if ((type(layers) not in {list, tuple}) or (len(layers) < 2)):
        raise Exception(('A Merge should only be applied to a list of layers with at least 2 elements. Found: ' + str(layers)))
    if (tensor_indices is None):
        tensor_indices = [None for _ in range(len(layers))]
    input_shapes = []
    for (i, layer) in enumerate(layers):
        layer_output_shape = layer.get_output_shape_at(node_indices[i])
        if (type(layer_output_shape) is list):
            layer_output_shape = layer_output_shape[tensor_indices[i]]
        input_shapes.append(layer_output_shape)
    if (mode in {'sum', 'mul', 'ave', 'cos'}):
        input_shapes_set = set(input_shapes)
        if (len(input_shapes_set) > 1):
            raise Exception(((('Only layers of same output shape can be merged using ' + mode) + ' mode. ') + ('Layer shapes: %s' % input_shapes)))
    if (mode in {'cos', 'dot'}):
        if (len(layers) > 2):
            raise Exception((mode + ' merge takes exactly 2 layers'))
        shape1 = input_shapes[0]
        shape2 = input_shapes[1]
        n1 = len(shape1)
        n2 = len(shape2)
        if (mode == 'dot'):
            if (type(dot_axes) == int):
                if (dot_axes < 0):
                    dot_axes = [(dot_axes % n1), (dot_axes % n2)]
                else:
                    dot_axes = [(n1 - dot_axes), (n2 - dot_axes)]
            if (type(dot_axes) not in [list, tuple]):
                raise Exception('Invalid type for dot_axes - should be a list.')
            if (len(dot_axes) != 2):
                raise Exception('Invalid format for dot_axes - should contain two elements.')
            if ((type(dot_axes[0]) is not int) or (type(dot_axes[1]) is not int)):
                raise Exception('Invalid format for dot_axes - list elements should be "int".')
            if (shape1[dot_axes[0]] != shape2[dot_axes[1]]):
                raise Exception((('Dimension incompatibility using dot mode: ' + ('%s != %s. ' % (shape1[dot_axes[0]], shape2[dot_axes[1]]))) + ('Layer shapes: %s, %s' % (shape1, shape2))))
    elif (mode == 'concat'):
        reduced_inputs_shapes = [list(shape) for shape in input_shapes]
        shape_set = set()
        for i in range(len(reduced_inputs_shapes)):
            del reduced_inputs_shapes[i][self.concat_axis]
            shape_set.add(tuple(reduced_inputs_shapes[i]))
        if (len(shape_set) > 1):
            raise Exception((('"concat" mode can only merge layers with matching ' + 'output shapes except for the concat axis. ') + ('Layer shapes: %s' % input_shapes)))