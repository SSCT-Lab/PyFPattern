

def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True), display_text=dict(default=None), url=dict(default=None), vm=dict(default=None), snapshot=dict(default=None), os_type=dict(default=None), is_ready=dict(type='bool', default=False), is_public=dict(type='bool', default=True), is_featured=dict(type='bool', default=False), is_dynamically_scalable=dict(type='bool', default=False), is_extractable=dict(type='bool', default=False), is_routing=dict(type='bool', default=None), checksum=dict(default=None), template_filter=dict(default='self', choices=['featured', 'self', 'selfexecutable', 'sharedexecutable', 'executable', 'community']), hypervisor=dict(choices=CS_HYPERVISORS, default=None), requires_hvm=dict(type='bool', default=False), password_enabled=dict(type='bool', default=False), template_tag=dict(default=None), sshkey_enabled=dict(type='bool', default=False), format=dict(choices=['QCOW2', 'RAW', 'VHD', 'OVA'], default=None), details=dict(default=None), bits=dict(type='int', choices=[32, 64], default=64), state=dict(choices=['present', 'absent', 'extracted'], default='present'), cross_zones=dict(type='bool', default=False), mode=dict(choices=['http_download', 'ftp_upload'], default='http_download'), zone=dict(default=None), domain=dict(default=None), account=dict(default=None), project=dict(default=None), poll_async=dict(type='bool', default=True), tags=dict(type='list', aliases=['tag'], default=None)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), mutually_exclusive=(['url', 'vm'], ['zone', 'cross_zones']), supports_check_mode=True)
    try:
        acs_tpl = AnsibleCloudStackTemplate(module)
        state = module.params.get('state')
        if (state in ['absent']):
            tpl = acs_tpl.remove_template()
        elif (state in ['extracted']):
            tpl = acs_tpl.extract_template()
        elif module.params.get('url'):
            tpl = acs_tpl.register_template()
        elif module.params.get('vm'):
            tpl = acs_tpl.create_template()
        else:
            module.fail_json(msg='one of the following is required on state=present: url,vm')
        result = acs_tpl.get_result(tpl)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)
