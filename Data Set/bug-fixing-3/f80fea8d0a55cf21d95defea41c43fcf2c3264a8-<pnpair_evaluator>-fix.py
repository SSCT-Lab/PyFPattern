@evaluator(EvaluatorAttribute.FOR_RANK)
@wrap_name_default()
def pnpair_evaluator(input, label, info, weight=None, name=None):
    '\n    Positive-negative pair rate Evaluator which adapts to rank task like\n    learning to rank. This evaluator must contain at least three layers.\n\n    The simple usage:\n\n    .. code-block:: python\n\n       eval = pnpair_evaluator(input, label, info)\n\n    :param input: Input Layer name. The output prediction of network.\n    :type input: LayerOutput\n    :param label: Label layer name.\n    :type label: LayerOutput\n    :param info: Info layer name. (TODO, explaination)\n    :type info: LayerOutput\n    :param weight: Weight Layer name. It should be a matrix with size\n                  [sample_num, 1]. (TODO, explaination)\n    :type weight: LayerOutput\n    :param name: Evaluator name.\n    :type name: None|basestring\n    '
    if (not isinstance(input, list)):
        input = [input]
    if label:
        input.append(label)
    if info:
        input.append(info)
    evaluator_base(input=input, type='pnpair', weight=weight, name=name)