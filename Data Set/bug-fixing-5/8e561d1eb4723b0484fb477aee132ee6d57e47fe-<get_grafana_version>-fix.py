def get_grafana_version(module, grafana_url, headers):
    grafana_version = None
    (r, info) = fetch_url(module, ('%s/api/frontend/settings' % grafana_url), headers=headers, method='GET')
    if (info['status'] == 200):
        try:
            settings = json.loads(r.read())
            grafana_version = str.split(settings['buildInfo']['version'], '.')[0]
        except Exception as e:
            raise GrafanaAPIException(e)
    else:
        raise GrafanaAPIException(('Unable to get grafana version : %s' % info))
    return int(grafana_version)