def generate_conn_array_dict(array):
    conn_array_info = {
        
    }
    api_version = array._list_available_rest_versions()
    carrays = array.list_array_connections()
    for carray in range(0, len(carrays)):
        arrayname = carrays[carray]['array_name']
        conn_array_info[arrayname] = {
            'array_id': carrays[carray]['id'],
            'throttled': carrays[carray]['throttled'],
            'version': carrays[carray]['version'],
            'type': carrays[carray]['type'],
            'mgmt_ip': carrays[carray]['management_address'],
            'repl_ip': carrays[carray]['replication_address'],
        }
        if (P53_API_VERSION in api_version):
            conn_array_info[arrayname]['status'] = carrays[carray]['status']
    throttles = array.list_array_connections(throttle=True)
    for throttle in range(0, len(throttles)):
        arrayname = throttles[throttle]['array_name']
        if conn_array_info[arrayname]['throttled']:
            conn_array_info[arrayname]['throttling'] = {
                'default_limit': throttles[throttle]['default_limit'],
                'window_limit': throttles[throttle]['window_limit'],
                'window': throttles[throttle]['window'],
            }
    return conn_array_info