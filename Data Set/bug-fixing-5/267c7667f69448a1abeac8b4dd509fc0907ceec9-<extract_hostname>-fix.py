def extract_hostname(server_info):
    try:
        return server_info['hostname']
    except (KeyError, TypeError):
        return None