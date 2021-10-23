def main():
    argument_spec = rax_argument_spec()
    argument_spec.update(dict(device=dict(required=True), volume=dict(required=True), server=dict(required=True), state=dict(default='present', choices=['present', 'absent']), wait=dict(type='bool', default=False), wait_timeout=dict(type='int', default=300)))
    module = AnsibleModule(argument_spec=argument_spec, required_together=rax_required_together())
    if (not HAS_PYRAX):
        module.fail_json(msg='pyrax is required for this module')
    device = module.params.get('device')
    volume = module.params.get('volume')
    server = module.params.get('server')
    state = module.params.get('state')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    setup_rax_module(module, pyrax)
    cloud_block_storage_attachments(module, state, volume, server, device, wait, wait_timeout)