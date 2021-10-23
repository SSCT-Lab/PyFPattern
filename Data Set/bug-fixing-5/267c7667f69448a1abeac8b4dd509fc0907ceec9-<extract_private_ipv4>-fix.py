def extract_private_ipv4(server_info):
    try:
        return server_info['private_ip']
    except (KeyError, TypeError):
        return None