def finish(module, tree, xpath, namespaces, changed=False, msg='', hitcount=0, matches=tuple()):
    result = dict(actions=dict(xpath=xpath, namespaces=namespaces, state=module.params['state']), changed=changed, count=hitcount, matches=matches, msg=msg)
    if (changed and module._diff):
        result['diff'] = dict(before=etree.tostring(orig_doc, xml_declaration=True, encoding='UTF-8', pretty_print=module.params['pretty_print']), after=etree.tostring(tree, xml_declaration=True, encoding='UTF-8', pretty_print=module.params['pretty_print']))
    if (module.params['path'] and (not module.check_mode)):
        if module.params['backup']:
            result['backup_file'] = module.backup_local(module.params['path'])
        tree.write(module.params['path'], xml_declaration=True, encoding='UTF-8', pretty_print=module.params['pretty_print'])
    if module.params['xmlstring']:
        result['xmlstring'] = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', pretty_print=module.params['pretty_print'])
    module.exit_json(**result)