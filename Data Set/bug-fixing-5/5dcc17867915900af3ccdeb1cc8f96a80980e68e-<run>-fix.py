def run(self):
    result = {
        'nginx_status_facts': {
            'active_connections': None,
            'accepts': None,
            'handled': None,
            'requests': None,
            'reading': None,
            'writing': None,
            'waiting': None,
            'data': None,
        },
    }
    (response, info) = fetch_url(module=module, url=self.url, force=True, timeout=self.timeout)
    if (not response):
        module.fail_json(msg=('No valid or no response from url %s within %s seconds (timeout)' % (self.url, self.timeout)))
    data = to_text(response.read(), errors='surrogate_or_strict')
    if (not data):
        return result
    result['nginx_status_facts']['data'] = data
    expr = 'Active connections: ([0-9]+) \\nserver accepts handled requests\\n ([0-9]+) ([0-9]+) ([0-9]+) \\nReading: ([0-9]+) Writing: ([0-9]+) Waiting: ([0-9]+)'
    match = re.match(expr, data, re.S)
    if match:
        result['nginx_status_facts']['active_connections'] = int(match.group(1))
        result['nginx_status_facts']['accepts'] = int(match.group(2))
        result['nginx_status_facts']['handled'] = int(match.group(3))
        result['nginx_status_facts']['requests'] = int(match.group(4))
        result['nginx_status_facts']['reading'] = int(match.group(5))
        result['nginx_status_facts']['writing'] = int(match.group(6))
        result['nginx_status_facts']['waiting'] = int(match.group(7))
    return result