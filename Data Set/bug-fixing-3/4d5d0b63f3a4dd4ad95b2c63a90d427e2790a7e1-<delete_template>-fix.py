def delete_template(meraki, org_id, name, data):
    template_id = get_template_id(meraki, name, data)
    path = meraki.construct_path('delete', org_id=org_id)
    path = ((path + '/') + template_id)
    response = meraki.request(path, 'DELETE')
    return response