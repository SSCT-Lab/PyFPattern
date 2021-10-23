def _retrieve_servers(api_key):
    api_url = 'https://api.vultr.com/v1/server/list'
    try:
        response = open_url(api_url, headers={
            'API-Key': api_key,
            'Content-type': 'application/json',
        }, http_agent=VULTR_USER_AGENT)
        servers_list = json.loads(response.read())
        if (not servers_list):
            return []
        return [server for (id, server) in servers_list.items()]
    except ValueError as e:
        raise AnsibleError('Incorrect JSON payload')
    except Exception as e:
        raise AnsibleError(('Error while fetching %s: %s' % (api_url, to_native(e))))