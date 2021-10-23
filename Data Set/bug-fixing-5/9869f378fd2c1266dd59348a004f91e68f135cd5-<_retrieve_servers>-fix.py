def _retrieve_servers(api_key):
    api_url = ('%s/v1/server/list' % VULTR_API_ENDPOINT)
    try:
        response = open_url(api_url, headers={
            'API-Key': api_key,
            'Content-type': 'application/json',
        }, http_agent=VULTR_USER_AGENT)
        servers_list = json.loads(response.read())
        return (servers_list.values() if servers_list else [])
    except ValueError:
        raise AnsibleError('Incorrect JSON payload')
    except Exception as e:
        raise AnsibleError(('Error while fetching %s: %s' % (api_url, to_native(e))))