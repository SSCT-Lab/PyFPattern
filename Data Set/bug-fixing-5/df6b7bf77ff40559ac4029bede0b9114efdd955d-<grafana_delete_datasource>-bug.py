def grafana_delete_datasource(module, data):
    headers = grafana_headers(module, data)
    (datasource_exists, ds) = grafana_datasource_exists(module, data['grafana_url'], data['name'], headers=headers)
    result = {
        
    }
    if (datasource_exists is True):
        (r, info) = fetch_url(module, ('%s/api/datasources/name/%s' % (data['grafana_url'], data['name'])), headers=headers, method='DELETE')
        if (info['status'] == 200):
            res = json.loads(to_text(r.read(), errors='surrogate_or_strict'))
            result['msg'] = ('Datasource %s deleted : %s' % (data['name'], res['message']))
            result['changed'] = True
            result['name'] = data['name']
            result['id'] = 0
        else:
            raise GrafanaAPIException(('Unable to update the datasource id %s : %s' % (ds['id'], info)))
    else:
        result = {
            'msg': ('Datasource %s does not exist.' % data['name']),
            'changed': False,
            'id': 0,
            'name': data['name'],
        }
    return result