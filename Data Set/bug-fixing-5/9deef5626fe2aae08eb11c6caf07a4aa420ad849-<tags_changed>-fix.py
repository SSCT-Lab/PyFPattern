def tags_changed(pcx_id, client, module):
    changed = False
    tags = dict()
    if module.params.get('tags'):
        tags = module.params.get('tags')
    pcx = find_pcx_by_id(pcx_id, client, module)
    if pcx['VpcPeeringConnections']:
        pcx_values = [t.values() for t in pcx['VpcPeeringConnections'][0]['Tags']]
        pcx_tags = [item for sublist in pcx_values for item in sublist]
        tag_values = [[key, str(value)] for (key, value) in tags.items()]
        tags = [item for sublist in tag_values for item in sublist]
        if (sorted(pcx_tags) == sorted(tags)):
            changed = False
        elif tags:
            delete_tags(pcx_id, client, module)
            create_tags(pcx_id, client, module)
            changed = True
    return changed