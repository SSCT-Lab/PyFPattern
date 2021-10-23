def outputs(layers, *args):
    '\n    Declare the outputs of network. If user have not defined the inputs of\n    network, this method will calculate the input order by dfs travel.\n\n    :param layers: Output layers.\n    :type layers: list|tuple|LayerOutput\n    :return:\n    '
    traveled = set()

    def __dfs_travel__(layer, predicate=(lambda x: (x.layer_type == LayerType.DATA))):
        '\n        DFS LRV Travel for output layer.\n\n        The return order is define order for data_layer in this leaf node.\n\n        :param layer:\n        :type layer: LayerOutput\n        :return:\n        '
        if (layer in traveled):
            return []
        else:
            traveled.add(layer)
        assert isinstance(layer, LayerOutput), ('layer is %s' % layer)
        retv = []
        if (layer.parents is not None):
            for p in layer.parents:
                retv.extend(__dfs_travel__(p, predicate))
        if predicate(layer):
            retv.append(layer)
        return retv
    if isinstance(layers, LayerOutput):
        layers = [layers]
    if (len(args) != 0):
        layers.extend(args)
    assert (len(layers) > 0)
    if HasInputsSet():
        Outputs(*[l.name for l in layers])
        return
    if (len(layers) != 1):
        logger.warning("`outputs` routine try to calculate network's inputs and outputs order. It might not work well.Please see follow log carefully.")
    inputs = []
    outputs_ = []
    for each_layer in layers:
        assert isinstance(each_layer, LayerOutput)
        inputs.extend(__dfs_travel__(each_layer))
        outputs_.extend(__dfs_travel__(each_layer, (lambda x: (x.layer_type == LayerType.COST))))
    final_inputs = []
    final_outputs = []
    for each_input in inputs:
        assert isinstance(each_input, LayerOutput)
        if (each_input.name not in final_inputs):
            final_inputs.append(each_input.name)
    for each_output in outputs_:
        assert isinstance(each_output, LayerOutput)
        if (each_output.name not in final_outputs):
            final_outputs.append(each_output.name)
    logger.info(''.join(['The input order is [', ', '.join(final_inputs), ']']))
    if (len(final_outputs) == 0):
        final_outputs = map((lambda x: x.name), layers)
    logger.info(''.join(['The output order is [', ', '.join(final_outputs), ']']))
    Inputs(*final_inputs)
    Outputs(*final_outputs)