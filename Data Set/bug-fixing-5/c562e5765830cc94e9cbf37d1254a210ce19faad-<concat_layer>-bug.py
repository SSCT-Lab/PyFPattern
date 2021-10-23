@wrap_act_default(act=IdentityActivation())
@wrap_name_default('concat')
@layer_support()
def concat_layer(input, act=None, name=None, layer_attr=None, bias_attr=None):
    '\n    Concat all input vector into one huge vector.\n    Inputs can be list of LayerOutput or list of projection.\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        concat = concat_layer(input=[layer1, layer2])\n\n    :param name: Layer name.\n    :type name: basestring\n    :param input: input layers or projections\n    :type input: list|tuple|collections.Sequence\n    :param act: Activation type.\n    :type act: BaseActivation\n    :param layer_attr: Extra Layer Attribute.\n    :type layer_attr: ExtraLayerAttribute\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    '
    if isinstance(input, LayerOutput):
        input = [input]
    elif isinstance(input, Projection):
        input = [input]
    else:
        assert isinstance(input, collections.Sequence)

    def __is_type__(o, tp):
        if (not isinstance(o, collections.Sequence)):
            if (o == tp):
                return True
            elif (len(o.__bases__) == 0):
                return False
            else:
                for bs in o.__bases__:
                    if __is_type__(bs, tp):
                        return True
                return False
        else:
            tmp = map((lambda _x: __is_type__(_x, tp)), o)
            a = tmp[0]
            for b in tmp[1:]:
                assert (a == b)
            return a

    def __reduce_concat_type__(a, b):
        assert (__is_type__([a, b], Projection) or __is_type__([a, b], LayerOutput))
        return a
    is_concat_layer = __is_type__(reduce(__reduce_concat_type__, map(type, input)), LayerOutput)
    layer_type = (LayerType.CONCAT_LAYER if is_concat_layer else LayerType.CONCAT_PROJ_LAYER)
    if (layer_type == LayerType.CONCAT_LAYER):
        assert (not bias_attr)
    Layer(name=name, type=layer_type, inputs=([x.name for x in input] if is_concat_layer else input), active_type=act.name, bias=ParamAttr.to_bias(bias_attr), **ExtraLayerAttribute.to_kwargs(layer_attr))
    sz = 0
    for each_input in input:
        if (each_input.size is not None):
            sz += each_input.size
        else:
            sz = None
            break
    return LayerOutput(name, layer_type=layer_type, parents=(input if is_concat_layer else [x.origin for x in input]), activation=act, size=sz)