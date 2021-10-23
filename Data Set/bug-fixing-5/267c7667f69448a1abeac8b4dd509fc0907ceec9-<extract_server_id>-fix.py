def extract_server_id(server_info):
    try:
        return server_info['id']
    except (KeyError, TypeError):
        return None