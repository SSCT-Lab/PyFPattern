def main():
    ' Main entry point for module execution\n    '
    option_spec = dict(name=dict(), num=dict(type='int'), value=dict(required=True), use_option=dict(type='bool', default=True), vendor_class=dict(default='DHCP'))
    ib_spec = dict(network=dict(required=True, aliases=['name', 'cidr'], ib_req=True), network_view=dict(default='default', ib_req=True), options=dict(type='list', elements='dict', options=option_spec, transform=options), extattrs=dict(type='dict'), comment=dict())
    argument_spec = dict(provider=dict(required=True), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(ib_spec)
    argument_spec.update(WapiModule.provider_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    obj_filter = dict([(k, module.params[k]) for (k, v) in iteritems(ib_spec) if v.get('ib_req')])
    network_type = check_ip_addr_type(obj_filter['network'])
    wapi = WapiModule(module)
    ib_spec = check_vendor_specific_dhcp_option(module, ib_spec)
    result = wapi.run(network_type, ib_spec)
    module.exit_json(**result)