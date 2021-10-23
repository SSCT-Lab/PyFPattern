def sync_docs(quiet=False):
    if (not quiet):
        echo('syncing documentation (platform index)')
    body = urlopen_with_retries(BASE_URL.format('_index.json')).read().decode('utf-8')
    data = json.loads(body)
    platform_list = []
    for (platform_id, integrations) in iteritems(data['platforms']):
        platform_list.append({
            'id': platform_id,
            'name': integrations['_self']['name'],
            'integrations': [{
                'id': get_integration_id(platform_id, i_id),
                'name': i_data['name'],
                'type': i_data['type'],
                'link': i_data['doc_link'],
            } for (i_id, i_data) in sorted(iteritems(integrations), key=(lambda x: x[1]['name']))],
        })
    platform_list.sort(key=(lambda x: x['name']))
    dump_doc('_platforms', {
        'platforms': platform_list,
    })
    for (platform_id, platform_data) in iteritems(data['platforms']):
        for (integration_id, integration) in iteritems(platform_data):
            sync_integration_docs(platform_id, integration_id, integration['details'], quiet)