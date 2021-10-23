def set_target_inner(module, tree, xpath, namespaces, attribute, value):
    changed = False
    try:
        if (not is_node(tree, xpath, namespaces)):
            changed = check_or_make_target(module, tree, xpath, namespaces)
    except Exception as e:
        missing_namespace = ''
        if ((len(tree.getroot().nsmap) > 0) and (':' not in xpath)):
            missing_namespace = 'XML document has namespace(s) defined, but no namespace prefix(es) used in xpath!\n'
        module.fail_json(msg=('%sXpath %s causes a failure: %s\n  -- tree is %s' % (missing_namespace, xpath, e, etree.tostring(tree, pretty_print=True))), exception=traceback.format_exc())
    if (not is_node(tree, xpath, namespaces)):
        module.fail_json(msg=('Xpath %s does not reference a node! tree is %s' % (xpath, etree.tostring(tree, pretty_print=True))))
    for element in tree.xpath(xpath, namespaces=namespaces):
        if (not attribute):
            changed = (changed or (element.text != value))
            if (element.text != value):
                element.text = value
        else:
            changed = (changed or (element.get(attribute) != value))
            if (':' in attribute):
                (attr_ns, attr_name) = attribute.split(':')
                attribute = '{{{0}}}{1}'.format(namespaces[attr_ns], attr_name)
            if (element.get(attribute) != value):
                element.set(attribute, value)
    return changed