def main():
    module = AnsibleModule(argument_spec=dict(auth_token=dict(default=os.environ.get(PACKET_API_TOKEN_ENV_VAR), no_log=True), count=dict(type='int', default=1), count_offset=dict(type='int', default=1), device_ids=dict(type='list'), facility=dict(), features=dict(type='dict'), hostnames=dict(type='list', aliases=['name']), locked=dict(type='bool', default=False, aliases=['lock']), operating_system=dict(), plan=dict(), project_id=dict(required=True), state=dict(choices=ALLOWED_STATES, default='present'), user_data=dict(default=None), wait_for_public_IPv=dict(type='int', choices=[4, 6]), wait_timeout=dict(type='int', default=900), ipxe_script_url=dict(default=''), always_pxe=dict(type='bool', default=False)), required_one_of=[('device_ids', 'hostnames')], mutually_exclusive=[('hostnames', 'device_ids'), ('count', 'device_ids'), ('count_offset', 'device_ids')])
    if (not HAS_PACKET_SDK):
        module.fail_json(msg='packet required for this module')
    if (not module.params.get('auth_token')):
        _fail_msg = ('if Packet API token is not in environment variable %s, the auth_token parameter is required' % PACKET_API_TOKEN_ENV_VAR)
        module.fail_json(msg=_fail_msg)
    auth_token = module.params.get('auth_token')
    packet_conn = packet.Manager(auth_token=auth_token)
    state = module.params.get('state')
    try:
        module.exit_json(**act_on_devices(module, packet_conn, state))
    except Exception as e:
        module.fail_json(msg=('failed to set device state %s, error: %s' % (state, to_native(e))), exception=traceback.format_exc())