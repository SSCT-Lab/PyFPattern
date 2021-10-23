def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(name=dict(required=True), url=dict(default=None), os_type=dict(default=None), zone=dict(default=None), iso_filter=dict(default='self', choices=['featured', 'self', 'selfexecutable', 'sharedexecutable', 'executable', 'community']), domain=dict(default=None), account=dict(default=None), project=dict(default=None), checksum=dict(default=None), is_ready=dict(type='bool', default=False), bootable=dict(type='bool', default=True), is_featured=dict(type='bool', default=False), is_dynamically_scalable=dict(type='bool', default=False), state=dict(choices=['present', 'absent'], default='present'), poll_async=dict(type='bool', default=True)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=cs_required_together(), supports_check_mode=True)
    try:
        acs_iso = AnsibleCloudStackIso(module)
        state = module.params.get('state')
        if (state in ['absent']):
            iso = acs_iso.remove_iso()
        else:
            iso = acs_iso.register_iso()
        result = acs_iso.get_result(iso)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)