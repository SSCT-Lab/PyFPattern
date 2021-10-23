def dropout(x, dropout_prob, is_test=False, seed=None, name=None, dropout_implementation='downgrade_in_infer'):
    '\n    Computes dropout.\n\n    Drop or keep each element of `x` independently. Dropout is a regularization\n    technique for reducing overfitting by preventing neuron co-adaption during\n    training. The dropout operator randomly sets (according to the given dropout\n    probability) the outputs of some units to zero, while others are remain\n    unchanged.\n\n    dropout op can be removed from the program to make the program more efficient.\n\n    Args:\n        x (Variable): The input tensor variable.\n        dropout_prob (float): Probability of setting units to zero.\n        is_test (bool): A flag indicating whether it is in test phrase or not.\n        seed (int): A Python integer used to create random seeds. If this\n                    parameter is set to None, a random seed is used.\n                    NOTE: If an integer seed is given, always the same output\n                    units will be dropped. DO NOT use a fixed seed in training.\n        name (str|None): A name for this layer(optional). If set None, the layer\n                         will be named automatically.\n        dropout_implementation(string): [\'downgrade_in_infer\'(default)|\'upscale_in_train\']\n\n                                        1. downgrade_in_infer(default), downgrade the outcome at inference\n\n                                           - train: out = input * mask\n                                           - inference: out = input * (1.0 - dropout_prob)\n\n                                           (mask is a tensor same shape with input, value is 0 or 1\n                                           ratio of 0 is dropout_prob)\n                                        2. upscale_in_train, upscale the outcome at training time\n\n                                           - train: out = input * mask / ( 1.0 - dropout_prob )\n                                           - inference: out = input\n\n                                           (mask is a tensor same shape with input, value is 0 or 1\n                                           ratio of 0 is dropout_prob)\n\n\n    Returns:\n        Variable: A tensor variable is the shape with `x`.\n\n    Examples:\n\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            x = fluid.layers.data(name="data", shape=[32, 32], dtype="float32")\n            droped = fluid.layers.dropout(x, dropout_prob=0.5)\n    '
    helper = LayerHelper('dropout', **locals())
    out = helper.create_variable_for_type_inference(dtype=x.dtype)
    mask = helper.create_variable_for_type_inference(dtype=core.VarDesc.VarType.UINT8, stop_gradient=True)
    if (((seed is None) or (seed == 0)) and (helper.main_program.random_seed != 0)):
        seed = helper.main_program.random_seed
    helper.append_op(type='dropout', inputs={
        'X': [x],
    }, outputs={
        'Out': [out],
        'Mask': [mask],
    }, attrs={
        'dropout_prob': dropout_prob,
        'is_test': is_test,
        'fix_seed': (seed is not None),
        'seed': (seed if (seed is not None) else 0),
        'dropout_implementation': dropout_implementation,
    })
    return out