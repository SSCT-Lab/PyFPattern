def add_elementwise(self, name, input_names, output_name, mode, alpha=None):
    "\n        Add an element-wise operation layer to the model.\n\n        Parameters\n        ----------\n            The name of this layer\n        name: str\n        input_names: [str]\n            A list of input blob names of this layer. The input blobs should have the same shape.\n        output_name: str\n            The output blob name of this layer.\n        mode: str\n            A string specifying the mode of the elementwise layer. It can be one of the following:\n\n            - 'CONCAT': concatenate input blobs along the channel axis.\n            - 'SEQUENCE_CONCAT': concatenate input blobs along the sequence axis.\n            - 'ADD': perform an element-wise summation over the input blobs.\n            - 'MULTIPLY': perform an element-wise multiplication over the input blobs.\n            - 'DOT': compute the dot product of the two input blobs. In this mode, the length of input_names should be 2.\n            - 'COS': compute the cosine similarity of the two input blobs. In this mode, the length of input_names should be 2.\n            - 'MAX': compute the element-wise maximum over the input blobs.\n            - 'MIN': compute the element-wise minimum over the input blobs.\n            - 'AVE': compute the element-wise average over the input blobs.\n        \n        alpha: float\n            if mode == 'ADD' and there is only one input_name, alpha is added to the input\n            if mode == 'MULTIPLY' and there is only one input_name, alpha is multiplied to the input\n       \n        See Also\n        --------\n        add_upsample, add_sequence_repeat\n       \n        "
    spec = self.spec
    nn_spec = self.nn_spec
    spec_layer = nn_spec.layers.add()
    spec_layer.name = name
    if isinstance(input_names, list):
        for input_name in input_names:
            spec_layer.input.append(input_name)
    else:
        spec_layer.input.append(input_names)
    spec_layer.output.append(output_name)
    if (mode == 'CONCAT'):
        spec_layer.concat.sequenceConcat = False
    elif (mode == 'SEQUENCE_CONCAT'):
        spec_layer.concat.sequenceConcat = True
    elif (mode == 'ADD'):
        spec_layer.add.MergeFromString('')
        if alpha:
            spec_layer.add.alpha = alpha
    elif (mode == 'MULTIPLY'):
        spec_layer.multiply.MergeFromString('')
        if alpha:
            spec_layer.add.alpha = alpha
    elif (mode == 'COS'):
        spec_layer.dot.cosineSimilarity = True
    elif (mode == 'DOT'):
        spec_layer.dot.cosineSimilarity = False
    elif (mode == 'MAX'):
        spec_layer.max.MergeFromString('')
    elif (mode == 'MIN'):
        spec_layer.min.MergeFromString('')
    elif (mode == 'AVE'):
        spec_layer.average.MergeFromString('')
    else:
        raise ValueError(('Unspported elementwise mode %s' % mode))