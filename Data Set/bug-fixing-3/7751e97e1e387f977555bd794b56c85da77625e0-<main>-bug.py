def main():
    'Main function'
    module = GcpModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), name=dict(required=True, type='str'), labels=dict(type='dict')))
    if (not module.params['scopes']):
        module.params['scopes'] = ['https://www.googleapis.com/auth/pubsub']
    state = module.params['state']
    fetch = fetch_resource(module, self_link(module))
    changed = False
    if fetch:
        if (state == 'present'):
            if is_different(module, fetch):
                update(module, self_link(module))
                fetch = fetch_resource(module, self_link(module))
                changed = True
        else:
            delete(module, self_link(module))
            fetch = {
                
            }
            changed = True
    elif (state == 'present'):
        fetch = create(module, self_link(module))
        changed = True
    else:
        fetch = {
            
        }
    fetch.update({
        'changed': changed,
    })
    module.exit_json(**fetch)