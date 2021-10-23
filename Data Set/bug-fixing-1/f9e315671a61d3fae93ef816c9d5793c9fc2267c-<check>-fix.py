

def check(module, name, state, service_id, integration_key, api_key, incident_key=None, http_call=fetch_url):
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Content-type': 'application/json',
        'Authorization': ('Token token=%s' % api_key),
        'Accept': 'application/vnd.pagerduty+json;version=2',
    }
    params = {
        'service_ids[]': service_id,
        'sort_by': 'incident_number:desc',
        'time_zone': 'UTC',
    }
    if incident_key:
        params['incident_key'] = incident_key
    url_parts = list(urlparse(url))
    url_parts[4] = urlencode(params, True)
    url = urlunparse(url_parts)
    (response, info) = http_call(module, url, method='get', headers=headers)
    if (info['status'] != 200):
        module.fail_json(msg=('failed to check current incident status.Reason: %s' % info['msg']))
    incidents = json.loads(response.read())['incidents']
    msg = 'No corresponding incident'
    if (len(incidents) == 0):
        if (state in ('acknowledged', 'resolved')):
            return (msg, False)
        return (msg, True)
    elif (state != incidents[0]['status']):
        return (incidents[0], True)
    return (incidents[0], False)
