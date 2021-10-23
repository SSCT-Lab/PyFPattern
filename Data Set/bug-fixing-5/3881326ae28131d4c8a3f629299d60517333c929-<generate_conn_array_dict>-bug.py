def generate_conn_array_dict(array):
    conn_array_info = {
        
    }
    api_version = array._list_available_rest_versions()
    if (CONN_STATUS_API_VERSION in api_version):
        carrays = array.list_connected_arrays()
        for carray in range(0, len(carrays)):
            arrayname = carrays[carray]['array_name']
            conn_array_info[arrayname] = {
                'array_id': carrays[carray]['id'],
                'throtled': carrays[carray]['throtled'],
                'version': carrays[carray]['version'],
                'type': carrays[carray]['type'],
                'mgmt_ip': carrays[carray]['management_address'],
                'repl_ip': carrays[carray]['replication_address'],
            }
            if (CONN_STATUS_API_VERSION in api_version):
                conn_array_info[arrayname]['status'] = carrays[carray]['status']
    return conn_array_info