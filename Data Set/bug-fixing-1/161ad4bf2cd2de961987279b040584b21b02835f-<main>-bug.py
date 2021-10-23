

def main():
    'Main function'
    module = GcpModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), name=dict(required=True, type='str'), description=dict(type='str'), accelerator_type=dict(required=True, type='str'), tensorflow_version=dict(required=True, type='str'), network=dict(type='str'), cidr_block=dict(required=True, type='str'), scheduling_config=dict(type='dict', options=dict(preemptible=dict(type='bool'))), labels=dict(type='dict'), zone=dict(required=True, type='str')))
    if (not module.params['scopes']):
        module.params['scopes'] = ['https://www.googleapis.com/auth/cloud-platform']
    state = module.params['state']
    fetch = fetch_resource(module, self_link(module))
    changed = False
    if fetch:
        if (state == 'present'):
            if is_different(module, fetch):
                update(module, self_link(module), fetch)
                fetch = fetch_resource(module, self_link(module))
                changed = True
        else:
            delete(module, self_link(module))
            fetch = {
                
            }
            changed = True
    elif (state == 'present'):
        fetch = create(module, create_link(module))
        changed = True
    else:
        fetch = {
            
        }
    fetch.update({
        'changed': changed,
    })
    module.exit_json(**fetch)
