def pretty(module, tree):
    xml_string = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', pretty_print=module.params['pretty_print'])
    result = dict(changed=False)
    if module.params['path']:
        xml_file = module.params['path']
        xml_content = open(xml_file)
        try:
            if (xml_string != xml_content.read()):
                result['changed'] = True
                if (not module.check_mode):
                    if module.params['backup']:
                        result['backup_file'] = module.backup_local(module.params['path'])
                    tree.write(xml_file, xml_declaration=True, encoding='UTF-8', pretty_print=module.params['pretty_print'])
        finally:
            xml_content.close()
    elif module.params['xmlstring']:
        result['xmlstring'] = xml_string
        if (xml_string != module.params['xmlstring']):
            result['changed'] = True
    module.exit_json(**result)