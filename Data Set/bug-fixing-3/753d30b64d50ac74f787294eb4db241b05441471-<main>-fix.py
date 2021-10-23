def main():
    module = AnsibleModule(argument_spec=dict(host=dict(type='str', required=True), port=dict(type='int', default=830), hostkey_verify=dict(type='bool', default=True), allow_agent=dict(type='bool', default=True), look_for_keys=dict(type='bool', default=True), datastore=dict(type='str', default='auto'), username=dict(type='str', required=True, no_log=True), password=dict(type='str', required=True, no_log=True), xml=dict(type='str', required=True)))
    if (not HAS_NCCLIENT):
        module.fail_json(msg='could not import the python library ncclient required by this module')
    try:
        xml.dom.minidom.parseString(module.params['xml'])
    except:
        e = get_exception()
        module.fail_json(msg=('error parsing XML: ' + str(e)))
        return
    nckwargs = dict(host=module.params['host'], port=module.params['port'], hostkey_verify=module.params['hostkey_verify'], allow_agent=module.params['allow_agent'], look_for_keys=module.params['look_for_keys'], username=module.params['username'], password=module.params['password'])
    retkwargs = dict()
    try:
        m = ncclient.manager.connect(**nckwargs)
    except ncclient.transport.errors.AuthenticationError:
        module.fail_json(msg='authentication failed while connecting to device')
    except:
        e = get_exception()
        module.fail_json(msg=('error connecting to the device: ' + str(e)))
        return
    retkwargs['server_capabilities'] = list(m.server_capabilities)
    if (module.params['datastore'] == 'candidate'):
        if (':candidate' in m.server_capabilities):
            datastore = 'candidate'
        else:
            m.close_session()
            module.fail_json(msg=':candidate is not supported by this netconf server')
    elif (module.params['datastore'] == 'running'):
        if (':writable-running' in m.server_capabilities):
            datastore = 'running'
        else:
            m.close_session()
            module.fail_json(msg=':writable-running is not supported by this netconf server')
    elif (module.params['datastore'] == 'auto'):
        if (':candidate' in m.server_capabilities):
            datastore = 'candidate'
        elif (':writable-running' in m.server_capabilities):
            datastore = 'running'
        else:
            m.close_session()
            module.fail_json(msg='neither :candidate nor :writable-running are supported by this netconf server')
    else:
        m.close_session()
        module.fail_json(msg=(module.params['datastore'] + ' datastore is not supported by this ansible module'))
    try:
        changed = netconf_edit_config(m=m, xml=module.params['xml'], commit=True, retkwargs=retkwargs, datastore=datastore)
    except:
        e = get_exception()
        module.fail_json(msg=('error editing configuration: ' + str(e)))
    finally:
        m.close_session()
    module.exit_json(changed=changed, **retkwargs)