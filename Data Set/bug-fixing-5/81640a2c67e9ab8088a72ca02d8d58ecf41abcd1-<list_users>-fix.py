def list_users(self):
    result = {
        
    }
    user_list = []
    users_results = []
    properties = ['Id', 'Name', 'UserName', 'RoleId', 'Locked', 'Enabled']
    response = self.get_request((self.root_uri + self.accounts_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for users in data['Members']:
        user_list.append(users['@odata.id'])
    for uri in user_list:
        user = {
            
        }
        response = self.get_request((self.root_uri + uri))
        if (response['ret'] is False):
            return response
        data = response['data']
        for property in properties:
            if (property in data):
                user[property] = data[property]
        users_results.append(user)
    result['entries'] = users_results
    return result