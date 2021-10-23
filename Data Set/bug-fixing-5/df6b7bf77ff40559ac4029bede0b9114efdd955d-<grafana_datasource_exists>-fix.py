def grafana_datasource_exists(module, grafana_url, name, headers):
    datasource_exists = False
    ds = {
        
    }
    (r, info) = fetch_url(module, ('%s/api/datasources/name/%s' % (grafana_url, quote(name))), headers=headers, method='GET')
    if (info['status'] == 200):
        datasource_exists = True
        ds = json.loads(to_text(r.read(), errors='surrogate_or_strict'))
    elif (info['status'] == 404):
        datasource_exists = False
    else:
        raise GrafanaAPIException(('Unable to get datasource %s : %s' % (name, info)))
    return (datasource_exists, ds)