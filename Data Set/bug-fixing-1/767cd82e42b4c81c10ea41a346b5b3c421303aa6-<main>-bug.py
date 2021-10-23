

def main():
    argument_spec = dict(state=dict(choices=['online', 'offline', 'restart', 'cleanup']), node=dict(default=None), timeout=dict(default=300, type='int'), force=dict(default=True, type='bool'))
    module = AnsibleModule(argument_spec, supports_check_mode=True)
    changed = False
    state = module.params['state']
    node = module.params['node']
    force = module.params['force']
    timeout = module.params['timeout']
    if (state in ['online', 'offline']):
        if (node is None):
            cluster_state = get_cluster_status(module)
            if (cluster_state == state):
                module.exit_json(changed=changed, out=cluster_state)
            else:
                set_cluster(module, state, timeout, force)
                cluster_state = get_cluster_status(module)
                if (cluster_state == state):
                    module.exit_json(changed=True, out=cluster_state)
                else:
                    module.fail_json(msg=('Fail to bring the cluster %s' % state))
        else:
            cluster_state = get_node_status(module, node)
            for node_state in cluster_state:
                if (node_state[1].strip().lower() == state):
                    module.exit_json(changed=changed, out=cluster_state)
                else:
                    set_cluster(module, state, timeout, force)
                    cluster_state = get_node_status(module, node)
                    module.exit_json(changed=True, out=cluster_state)
    if (state in ['restart']):
        set_cluster(module, 'offline', timeout, force)
        cluster_state = get_cluster_status(module)
        if (cluster_state == 'offline'):
            set_cluster(module, 'online', timeout, force)
            cluster_state = get_cluster_status(module)
            if (cluster_state == 'online'):
                module.exit_json(changed=True, out=cluster_state)
            else:
                module.fail_json(msg="Failed during the restart of the cluster, the cluster can't be started")
        else:
            module.fail_json(msg="Failed during the restart of the cluster, the cluster can't be stopped")
    if (state in ['cleanup']):
        set_cluster(module, state, timeout, force)
        module.exit_json(changed=True, out=cluster_state)
