def _host_is_ipv6_address(self, host):
    return (':' in to_text(host, errors='surrogate_or_strict'))