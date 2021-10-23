def main():
    'Main function'
    module = GcpModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), affinity_cookie_ttl_sec=dict(type='int'), backends=dict(type='list', elements='dict', options=dict(balancing_mode=dict(type='str', choices=['UTILIZATION', 'RATE', 'CONNECTION']), capacity_scaler=dict(type='str'), description=dict(type='str'), group=dict(type='dict'), max_connections=dict(type='int'), max_connections_per_instance=dict(type='int'), max_rate=dict(type='int'), max_rate_per_instance=dict(type='str'), max_utilization=dict(type='str'))), cdn_policy=dict(type='dict', options=dict(cache_key_policy=dict(type='dict', options=dict(include_host=dict(type='bool'), include_protocol=dict(type='bool'), include_query_string=dict(type='bool'), query_string_blacklist=dict(type='list', elements='str'), query_string_whitelist=dict(type='list', elements='str'))))), connection_draining=dict(type='dict', options=dict(draining_timeout_sec=dict(type='int'))), description=dict(type='str'), enable_cdn=dict(type='bool'), health_checks=dict(type='list', elements='str'), iap=dict(type='dict', options=dict(enabled=dict(type='bool'), oauth2_client_id=dict(type='str'), oauth2_client_secret=dict(type='str'), oauth2_client_secret_sha256=dict(type='str'))), load_balancing_scheme=dict(type='str', choices=['INTERNAL', 'EXTERNAL']), name=dict(type='str'), port_name=dict(type='str'), protocol=dict(type='str', choices=['HTTP', 'HTTPS', 'TCP', 'SSL']), region=dict(type='str'), session_affinity=dict(type='str', choices=['NONE', 'CLIENT_IP', 'GENERATED_COOKIE', 'CLIENT_IP_PROTO', 'CLIENT_IP_PORT_PROTO']), timeout_sec=dict(type='int', aliases=['timeout_seconds'])))
    if (not module.params['scopes']):
        module.params['scopes'] = ['https://www.googleapis.com/auth/compute']
    state = module.params['state']
    kind = 'compute#backendService'
    fetch = fetch_resource(module, self_link(module), kind)
    changed = False
    if fetch:
        if (state == 'present'):
            if is_different(module, fetch):
                fetch = update(module, self_link(module), kind)
                changed = True
        else:
            delete(module, self_link(module), kind)
            fetch = {
                
            }
            changed = True
    elif (state == 'present'):
        fetch = create(module, collection(module), kind)
        changed = True
    else:
        fetch = {
            
        }
    fetch.update({
        'changed': changed,
    })
    module.exit_json(**fetch)