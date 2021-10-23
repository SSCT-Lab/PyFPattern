

def _get_output(output, input, shape=None):
    if (shape is None):
        shape = input.shape
    if (output is None):
        output = numpy.zeros(shape, dtype=input.dtype.name)
    elif (type(output) in [type(type), type(numpy.zeros((4,)).dtype)]):
        output = numpy.zeros(shape, dtype=output)
    elif isinstance(output, string_types):
        output = numpy.typeDict[output]
        output = numpy.zeros(shape, dtype=output)
    elif (output.shape != shape):
        raise RuntimeError('output shape not correct')
    return output
