def identity_projection(input, offset=None):
    '\n    1. IdentityProjection if offset=None. It performs:\n\n    .. math::\n       out.row[i] += in.row[i]\n\n    The example usage is:\n\n    .. code-block:: python\n\n       proj = identity_projection(input=layer)\n\n\n    2. IdentityOffsetProjection if offset!=None. It likes IdentityProjection,\n    but layer size may be smaller than input size.\n    It select dimesions [offset, offset+layer_size) from input:\n\n    .. math::\n       out.row[i] += in.row[i + \\textrm{offset}]\n\n    The example usage is:\n\n    .. code-block:: python\n\n       proj = identity_projection(input=layer,\n                                  offset=10)\n\n    Note that both of two projections should not have any parameter.\n\n    :param input: Input Layer.\n    :type input: LayerOutput\n    :param offset: Offset, None if use default.\n    :type offset: int\n    :return: A IdentityProjection or IdentityOffsetProjection object\n    :rtype: IdentityProjection or IdentityOffsetProjection\n    '
    if (offset is None):
        proj = IdentityProjection(input_layer_name=input.name)
        proj.origin = input
    else:
        proj = IdentityOffsetProjection(input_layer_name=input.name, offset=offset)
        proj.origin = input
    return proj