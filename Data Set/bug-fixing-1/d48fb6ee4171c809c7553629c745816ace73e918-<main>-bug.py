

def main():
    argument_spec = scaleway_argument_spec()
    argument_spec.update(dict(image=dict(required=True), name=dict(), region=dict(required=True, choices=SCALEWAY_LOCATION.keys()), commercial_type=dict(required=True, choices=SCALEWAY_COMMERCIAL_TYPES), enable_ipv6=dict(default=False, type='bool'), public_ip=dict(default='absent'), state=dict(choices=state_strategy.keys(), default='present'), tags=dict(type='list', default=[]), organization=dict(required=True), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=300), wait_sleep_time=dict(type='int', default=3), security_group=dict()))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    core(module)
