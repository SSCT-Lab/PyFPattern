def format_item(self, item):
    d = item.as_dict()
    resource_group = d['id'].split('resourceGroups/')[1].split('/')[0]
    name = d['name']
    credentials = {
        
    }
    admin_user_enabled = d['admin_user_enabled']
    if (self.retrieve_credentials and admin_user_enabled):
        credentials = self.containerregistry_client.registries.list_credentials(resource_group, name).as_dict()
        for index in range(len(credentials['passwords'])):
            password = credentials['passwords'][index]
            if (password['name'] == 'password'):
                credentials['password'] = password['value']
            elif (password['name'] == 'password2'):
                credentials['password2'] = password['value']
        credentials.pop('passwords')
    d = {
        'resource_group': resource_group,
        'name': d['name'],
        'location': d['location'],
        'admin_user_enabled': admin_user_enabled,
        'sku': d['sku']['tier'].lower(),
        'provisioning_state': d['provisioning_state'],
        'login_server': d['login_server'],
        'id': d['id'],
        'tags': d.get('tags', None),
        'credentials': credentials,
    }
    return d