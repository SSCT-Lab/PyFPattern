def main():
    module = AnsibleModule(argument_spec=dict(path=dict(type='path', aliases=['dest', 'file']), xmlstring=dict(type='str'), xpath=dict(type='str'), namespaces=dict(type='dict', default={
        
    }), state=dict(type='str', default='present', choices=['absent', 'present'], aliases=['ensure']), value=dict(type='raw'), attribute=dict(type='raw'), add_children=dict(type='list'), set_children=dict(type='list'), count=dict(type='bool', default=False), print_match=dict(type='bool', default=False), pretty_print=dict(type='bool', default=False), content=dict(type='str', choices=['attribute', 'text']), input_type=dict(type='str', default='yaml', choices=['xml', 'yaml']), backup=dict(type='bool', default=False)), supports_check_mode=True, required_if=[['content', 'attribute', ['xpath']], ['content', 'text', ['xpath']], ['count', True, ['xpath']], ['print_match', True, ['xpath']]], required_one_of=[['path', 'xmlstring'], ['add_children', 'content', 'count', 'pretty_print', 'print_match', 'set_children', 'value']], mutually_exclusive=[['add_children', 'content', 'count', 'print_match', 'set_children', 'value'], ['path', 'xmlstring']])
    xml_file = module.params['path']
    xml_string = module.params['xmlstring']
    xpath = module.params['xpath']
    namespaces = module.params['namespaces']
    state = module.params['state']
    value = json_dict_bytes_to_unicode(module.params['value'])
    attribute = module.params['attribute']
    set_children = json_dict_bytes_to_unicode(module.params['set_children'])
    add_children = json_dict_bytes_to_unicode(module.params['add_children'])
    pretty_print = module.params['pretty_print']
    content = module.params['content']
    input_type = module.params['input_type']
    print_match = module.params['print_match']
    count = module.params['count']
    backup = module.params['backup']
    if (not HAS_LXML):
        module.fail_json(msg='The xml ansible module requires the lxml python library installed on the managed machine')
    elif (LooseVersion('.'.join((to_native(f) for f in etree.LXML_VERSION))) < LooseVersion('2.3.0')):
        module.fail_json(msg='The xml ansible module requires lxml 2.3.0 or newer installed on the managed machine')
    elif (LooseVersion('.'.join((to_native(f) for f in etree.LXML_VERSION))) < LooseVersion('3.0.0')):
        module.warn('Using lxml version lower than 3.0.0 does not guarantee predictable element attribute order.')
    if xml_string:
        infile = BytesIO(to_bytes(xml_string, errors='surrogate_or_strict'))
    elif os.path.isfile(xml_file):
        infile = open(xml_file, 'rb')
    else:
        module.fail_json(msg=("The target XML source '%s' does not exist." % xml_file))
    if (xpath is not None):
        try:
            etree.XPath(xpath)
        except etree.XPathSyntaxError as e:
            module.fail_json(msg=('Syntax error in xpath expression: %s (%s)' % (xpath, e)))
        except etree.XPathEvalError as e:
            module.fail_json(msg=('Evaluation error in xpath expression: %s (%s)' % (xpath, e)))
    try:
        parser = etree.XMLParser(remove_blank_text=pretty_print)
        doc = etree.parse(infile, parser)
    except etree.XMLSyntaxError as e:
        module.fail_json(msg=('Error while parsing document: %s (%s)' % ((xml_file or 'xml_string'), e)))
    global orig_doc
    orig_doc = copy.deepcopy(doc)
    if print_match:
        do_print_match(module, doc, xpath, namespaces)
    if count:
        count_nodes(module, doc, xpath, namespaces)
    if (content == 'attribute'):
        get_element_attr(module, doc, xpath, namespaces)
    elif (content == 'text'):
        get_element_text(module, doc, xpath, namespaces)
    if (state == 'absent'):
        delete_xpath_target(module, doc, xpath, namespaces)
    if set_children:
        set_target_children(module, doc, xpath, namespaces, set_children, input_type)
    if add_children:
        add_target_children(module, doc, xpath, namespaces, add_children, input_type)
    if (value is not None):
        set_target(module, doc, xpath, namespaces, attribute, value)
    if (xpath is not None):
        ensure_xpath_exists(module, doc, xpath, namespaces)
    if pretty_print:
        make_pretty(module, doc)
    module.fail_json(msg="Don't know what to do")