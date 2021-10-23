def main():
    'entry point for module execution\n    '
    argument_spec = dict(source=dict(choices=['running', 'candidate', 'startup']), filter=dict(), display=dict(choices=['json', 'pretty', 'xml']), lock=dict(default='never', choices=['never', 'always', 'if-supported']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    capabilities = get_capabilities(module)
    operations = capabilities['device_operations']
    source = module.params['source']
    filter = module.params['filter']
    filter_type = get_filter_type(filter)
    lock = module.params['lock']
    display = module.params['display']
    if ((source == 'candidate') and (not operations.get('supports_commit', False))):
        module.fail_json(msg='candidate source is not supported on this device')
    if ((source == 'startup') and (not operations.get('supports_startup', False))):
        module.fail_json(msg='startup source is not supported on this device')
    if ((filter_type == 'xpath') and (not operations.get('supports_xpath', False))):
        module.fail_json(msg=("filter value '%s' of type xpath is not supported on this device" % filter))
    execute_lock = (True if (lock in ('always', 'if-supported')) else False)
    if ((lock == 'always') and (not operations.get('supports_lock', False))):
        module.fail_json(msg='lock operation is not supported on this device')
    if execute_lock:
        if (source is None):
            if ('running' not in operations.get('lock_datastore', [])):
                if (lock == 'if-supported'):
                    execute_lock = False
                else:
                    module.warn("lock operation on 'running' source is not supported on this device")
        elif (source not in operations.get('lock_datastore', [])):
            if (lock == 'if-supported'):
                execute_lock = False
            else:
                module.warn(("lock operation on '%s' source is not supported on this device" % source))
    if ((display == 'json') and (not HAS_JXMLEASE)):
        module.fail_json(msg='jxmlease is required to display response in json formatbut does not appear to be installed. It can be installed using `pip install jxmlease`')
    filter_spec = ((filter_type, filter) if filter_type else None)
    if (source is not None):
        response = get_config(module, source, filter_spec, execute_lock)
    else:
        response = get(module, filter_spec, execute_lock)
    xml_resp = tostring(response)
    output = None
    if (display == 'xml'):
        output = remove_namespaces(xml_resp)
    elif (display == 'json'):
        try:
            output = jxmlease.parse(xml_resp)
        except:
            raise ValueError(xml_resp)
    elif (display == 'pretty'):
        output = tostring(response, pretty_print=True)
    result = {
        'stdout': xml_resp,
        'output': output,
    }
    module.exit_json(**result)