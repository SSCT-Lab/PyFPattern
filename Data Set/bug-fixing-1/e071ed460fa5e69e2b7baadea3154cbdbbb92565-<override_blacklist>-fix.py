

def override_blacklist(*ip_addresses):

    def decorator(func):

        def wrapper(*args, **kwargs):
            disallowed_ips = frozenset(net_socket.DISALLOWED_IPS)
            net_socket.DISALLOWED_IPS = frozenset((ipaddress.ip_network(six.text_type(ip)) for ip in ip_addresses))
            try:
                func(*args, **kwargs)
            finally:
                net_socket.DISALLOWED_IPS = disallowed_ips
                net_socket.is_ipaddress_allowed.cache_clear()
        return wrapper
    return decorator
