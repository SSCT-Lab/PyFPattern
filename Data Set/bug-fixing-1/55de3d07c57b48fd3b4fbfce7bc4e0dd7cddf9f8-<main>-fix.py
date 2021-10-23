

def main():
    ' Main entry point for module execution\n    '
    ipv4addr_spec = dict(ipv4addr=dict(required=True, aliases=['address'], ib_req=True), mac=dict())
    ipv6addr_spec = dict(ipv6addr=dict(required=True, aliases=['address'], ib_req=True))
    ib_spec = dict(name=dict(required=True, ib_req=True), view=dict(default='default', aliases=['dns_view'], ib_req=True), ipv4addrs=dict(type='list', aliases=['ipv4'], elements='dict', options=ipv4addr_spec, transform=ipv4addrs), ipv6addrs=dict(type='list', aliases=['ipv6'], elements='dict', options=ipv6addr_spec, transform=ipv6addrs), aliases=dict(type='list'), ttl=dict(type='int'), extattrs=dict(type='dict'), comment=dict())
    argument_spec = dict(provider=dict(required=True), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(ib_spec)
    argument_spec.update(WapiModule.provider_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    wapi = WapiModule(module)
    result = wapi.run(NIOS_HOST_RECORD, ib_spec)
    module.exit_json(**result)
