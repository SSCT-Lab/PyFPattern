def main():
    ' Main entry point for module execution\n    '
    grid_spec = dict(name=dict(required=True))
    ib_spec = dict(fqdn=dict(required=True, aliases=['name'], ib_req=True), view=dict(default='default', aliases=['dns_view'], ib_req=True), grid_primary=dict(type='list', elements='dict', options=grid_spec), grid_secondaries=dict(type='list', elements='dict', options=grid_spec), extattrs=dict(type='dict'), comment=dict())
    argument_spec = dict(provider=dict(required=True), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(ib_spec)
    argument_spec.update(WapiModule.provider_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    wapi = WapiModule(module)
    result = wapi.run('zone_auth', ib_spec)
    module.exit_json(**result)