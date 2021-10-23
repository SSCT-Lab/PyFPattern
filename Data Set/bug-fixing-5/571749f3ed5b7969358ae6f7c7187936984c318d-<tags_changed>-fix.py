def tags_changed(nacl_id, client, module):
    changed = False
    tags = dict()
    if module.params.get('tags'):
        tags = module.params.get('tags')
    if (module.params.get('name') and (not tags.get('Name'))):
        tags['Name'] = module.params['name']
    nacl = find_acl_by_id(nacl_id, client, module)
    if nacl['NetworkAcls']:
        nacl_values = [t.values() for t in nacl['NetworkAcls'][0]['Tags']]
        nacl_tags = [item for sublist in nacl_values for item in sublist]
        tag_values = [[key, str(value)] for (key, value) in tags.items()]
        tags = [item for sublist in tag_values for item in sublist]
        if (sorted(nacl_tags) == sorted(tags)):
            changed = False
            return changed
        else:
            delete_tags(nacl_id, client, module)
            create_tags(nacl_id, client, module)
            changed = True
            return changed
    return changed