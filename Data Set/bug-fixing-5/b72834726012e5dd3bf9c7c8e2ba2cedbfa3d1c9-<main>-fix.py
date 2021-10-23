def main():
    'Module main'
    argument_spec = dict(session_name=dict(required=True, type='str'), create_type=dict(required=False, default='static', type='str', choices=['static', 'auto']), addr_type=dict(required=False, type='str', choices=['ipv4']), out_if_name=dict(required=False, type='str'), dest_addr=dict(required=False, type='str'), src_addr=dict(required=False, type='str'), vrf_name=dict(required=False, type='str'), use_default_ip=dict(required=False, type='bool', default=False), state=dict(required=False, default='present', choices=['present', 'absent']), local_discr=dict(required=False, type='int'), remote_discr=dict(required=False, type='int'))
    argument_spec.update(ce_argument_spec)
    module = BfdSession(argument_spec)
    module.work()