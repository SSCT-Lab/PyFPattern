def main():
    module = AnsibleModule(argument_spec=dict(host=dict(type='str', required=True), port=dict(type='int', default=830), hostkey_verify=dict(type='bool', default=True), username=dict(type='str', required=True, no_log=True), password=dict(type='str', required=True, no_log=True), xml=dict(type='str', required=True)))
    if (not HAS_NCCLIENT):
        module.fail_json(msg='could not import the python library ncclient required by this module')
    try:
        xml.dom.minidom.parseString(module.params['xml'])
    except:
        e = get_exception()
        module.fail_json(msg=('error parsing XML: ' + str(e)))
        return
    nckwargs = dict(host=module.params['host'], port=module.params['port'], hostkey_verify=module.params['hostkey_verify'], username=module.params['username'], password=module.params['password'])
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
    try:
        changed = netconf_edit_config(m=m, xml=module.params['xml'], commit=True, retkwargs=retkwargs)
    finally:
        m.close_session()
    module.exit_json(changed=changed, **retkwargs)