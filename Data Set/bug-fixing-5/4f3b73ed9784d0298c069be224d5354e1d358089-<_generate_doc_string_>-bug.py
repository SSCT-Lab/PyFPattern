def _generate_doc_string_(op_proto):
    '\n    Generate docstring by OpProto\n\n    Args:\n        op_proto (framework_pb2.OpProto): a protobuf message typed OpProto\n\n    Returns:\n        str: the document string\n    '

    def _type_to_str_(tp):
        return framework_pb2.AttrType.Name(tp)
    if (not isinstance(op_proto, framework_pb2.OpProto)):
        raise TypeError('OpProto should be `framework_pb2.OpProto`')
    buf = cStringIO.StringIO()
    buf.write(op_proto.comment)
    buf.write('\nArgs:\n')
    for each_input in op_proto.inputs:
        line_begin = '    {0}: '.format(_convert_(each_input.name))
        buf.write(line_begin)
        buf.write(each_input.comment)
        buf.write('\n')
        buf.write((' ' * len(line_begin)))
        buf.write('Duplicable: ')
        buf.write(str(each_input.duplicable))
        buf.write('  Optional: ')
        buf.write(str(each_input.dispensable))
        buf.write('\n')
    for each_attr in op_proto.attrs:
        buf.write('    ')
        buf.write(each_attr.name)
        buf.write(' (')
        buf.write(_type_to_str_(each_attr.type))
        buf.write('): ')
        buf.write(each_attr.comment)
        buf.write('\n')
    if (len(op_proto.outputs) != 0):
        buf.write('\nReturns:\n')
        buf.write('    ')
        for each_opt in op_proto.outputs:
            if (not each_opt.intermediate):
                break
        buf.write(each_opt.comment)
    return buf.getvalue()