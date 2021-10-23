def grafana_create_datasource(module, data):
    payload = {
        'orgId': data['org_id'],
        'name': data['name'],
        'type': data['ds_type'],
        'access': data['access'],
        'url': data['url'],
        'database': data['database'],
        'withCredentials': data['with_credentials'],
        'isDefault': data['is_default'],
        'user': data['user'],
        'password': data['password'],
    }
    if (('basic_auth_user' in data) and data['basic_auth_user'] and ('basic_auth_password' in data) and data['basic_auth_password']):
        payload['basicAuth'] = True
        payload['basicAuthUser'] = data['basic_auth_user']
        payload['basicAuthPassword'] = data['basic_auth_password']
    else:
        payload['basicAuth'] = False
    json_data = {
        
    }
    if (data.get('tls_client_cert') and data.get('tls_client_key')):
        json_data['tlsAuth'] = True
        if data.get('tls_ca_cert'):
            payload['secureJsonData'] = {
                'tlsCACert': data['tls_ca_cert'],
                'tlsClientCert': data['tls_client_cert'],
                'tlsClientKey': data['tls_client_key'],
            }
            json_data['tlsAuthWithCACert'] = True
        else:
            payload['secureJsonData'] = {
                'tlsClientCert': data['tls_client_cert'],
                'tlsClientKey': data['tls_client_key'],
            }
    else:
        json_data['tlsAuth'] = False
        json_data['tlsAuthWithCACert'] = False
    if (data['ds_type'] == 'elasticsearch'):
        json_data['esVersion'] = data['es_version']
        json_data['timeField'] = data['time_field']
        if data.get('interval'):
            json_data['interval'] = data['interval']
        if (data['es_version'] >= 56):
            json_data['maxConcurrentShardRequests'] = data['max_concurrent_shard_requests']
    if ((data['ds_type'] == 'elasticsearch') or (data['ds_type'] == 'influxdb')):
        if data.get('time_interval'):
            json_data['timeInterval'] = data['time_interval']
    if (data['ds_type'] == 'opentsdb'):
        json_data['tsdbVersion'] = data['tsdb_version']
        if (data['tsdb_resolution'] == 'second'):
            json_data['tsdbResolution'] = 1
        else:
            json_data['tsdbResolution'] = 2
    if (data['ds_type'] == 'postgres'):
        json_data['sslmode'] = data['sslmode']
    payload['jsonData'] = json_data
    headers = {
        'content-type': 'application/json; charset=utf8',
    }
    if (('grafana_api_key' in data) and (data['grafana_api_key'] is not None)):
        headers['Authorization'] = ('Bearer %s' % data['grafana_api_key'])
    else:
        auth = base64.encodestring(('%s:%s' % (data['grafana_user'], data['grafana_password']))).replace('\n', '')
        headers['Authorization'] = ('Basic %s' % auth)
        grafana_switch_organisation(module, data['grafana_url'], data['org_id'], headers)
    (datasource_exists, ds) = grafana_datasource_exists(module, data['grafana_url'], data['name'], headers=headers)
    result = {
        
    }
    if (datasource_exists is True):
        del ds['typeLogoUrl']
        if (ds['basicAuth'] is False):
            del ds['basicAuthUser']
            del ds['basicAuthPassword']
        if ('jsonData' in ds):
            if (('tlsAuth' in ds['jsonData']) and (ds['jsonData']['tlsAuth'] is False)):
                del ds['secureJsonFields']
            if ('tlsAuth' not in ds['jsonData']):
                del ds['secureJsonFields']
        payload['id'] = ds['id']
        if (ds == payload):
            result['name'] = data['name']
            result['id'] = ds['id']
            result['msg'] = ('Datasource %s unchanged.' % data['name'])
            result['changed'] = False
        else:
            (r, info) = fetch_url(module, ('%s/api/datasources/%d' % (data['grafana_url'], ds['id'])), data=json.dumps(payload), headers=headers, method='PUT')
            if (info['status'] == 200):
                res = json.loads(r.read())
                result['name'] = data['name']
                result['id'] = ds['id']
                result['before'] = ds
                result['after'] = payload
                result['msg'] = ('Datasource %s updated %s' % (data['name'], res['message']))
                result['changed'] = True
            else:
                raise GrafanaAPIException(('Unable to update the datasource id %d : %s' % (ds['id'], info)))
    else:
        (r, info) = fetch_url(module, ('%s/api/datasources' % data['grafana_url']), data=json.dumps(payload), headers=headers, method='POST')
        if (info['status'] == 200):
            res = json.loads(r.read())
            result['msg'] = ('Datasource %s created : %s' % (data['name'], res['message']))
            result['changed'] = True
            result['name'] = data['name']
            result['id'] = res['id']
        else:
            raise GrafanaAPIException(('Unable to create the new datasource %s : %s - %s.' % (data['name'], info['status'], info)))
    return result