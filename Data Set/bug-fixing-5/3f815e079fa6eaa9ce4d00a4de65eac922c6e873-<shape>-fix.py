@templatedoc()
def shape(input):
    '\n    ${comment}\n\n    Args:\n        input (Variable): ${input_comment}\n\n    Returns:\n        out (Variable): ${out_comment}\n\n    Examples:\n        .. code-block:: python\n\n            input = layers.data(\n                name="input", shape=[3, 100, 100], dtype="float32")\n            out = layers.shape(input)\n    '
    helper = LayerHelper('shape', **locals())
    out = helper.create_variable_for_type_inference(dtype='int32')
    helper.append_op(type='shape', inputs={
        'Input': input,
    }, outputs={
        'Out': out,
    })
    return out