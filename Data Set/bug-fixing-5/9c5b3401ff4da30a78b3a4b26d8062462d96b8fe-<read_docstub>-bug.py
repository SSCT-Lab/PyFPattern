def read_docstub(filename):
    '\n    Quickly find short_description using string methods instead of node parsing.\n    This does not return a full set of documentation strings and is intended for\n    operations like ansible-doc -l.\n    '
    t_module_data = open(filename, 'r')
    in_documentation = False
    capturing = False
    indent_detection = ''
    doc_stub = []
    for line in t_module_data:
        if in_documentation:
            if (capturing and line.startswith(indent_detection)):
                doc_stub.append(line)
            elif (capturing and (not line.startswith(indent_detection))):
                break
            elif line.lstrip().startswith('short_description:'):
                capturing = True
                indent_detection = (' ' * ((len(line) - len(line.lstrip())) + 1))
                doc_stub.append(line)
        elif (line.startswith('DOCUMENTATION') and ('=' in line)):
            in_documentation = True
    short_description = ''.join(doc_stub).strip().rstrip('.')
    data = AnsibleLoader(short_description, file_name=filename).get_single_data()
    return data