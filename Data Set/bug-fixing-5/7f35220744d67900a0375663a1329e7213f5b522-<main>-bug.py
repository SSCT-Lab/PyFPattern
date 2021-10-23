def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(dict(ip_address=dict(default=None), network=dict(default=None), cidr=dict(default='0.0.0.0/0'), protocol=dict(choices=['tcp', 'udp', 'icmp', 'all'], default='tcp'), type=dict(choices=['ingress', 'egress'], default='ingress'), icmp_type=dict(type='int', default=None), icmp_code=dict(type='int', default=None), start_port=dict(type='int', aliases=['port'], default=None), end_port=dict(type='int', default=None), state=dict(choices=['present', 'absent'], default='present'), zone=dict(default=None), domain=dict(default=None), account=dict(default=None), project=dict(default=None), poll_async=dict(type='bool', default=True)))
    required_together = cs_required_together()
    required_together.extend([['icmp_type', 'icmp_code']])
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, required_one_of=(['ip_address', 'network'],), mutually_exclusive=(['icmp_type', 'start_port'], ['icmp_type', 'end_port'], ['ip_address', 'network']), supports_check_mode=True)
    try:
        acs_fw = AnsibleCloudStackFirewall(module)
        state = module.params.get('state')
        if (state in ['absent']):
            fw_rule = acs_fw.remove_firewall_rule()
        else:
            fw_rule = acs_fw.create_firewall_rule()
        result = acs_fw.get_result(fw_rule)
    except CloudStackException as e:
        module.fail_json(msg=('CloudStackException: %s' % str(e)))
    module.exit_json(**result)