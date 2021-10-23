def list_users(self):
    result = {
        
    }
    allusers = []
    allusers_details = []
    response = self.get_request((self.root_uri + self.accounts_uri))
    if (response['ret'] is False):
        return response
    result['ret'] = True
    data = response['data']
    for users in data['Members']:
        allusers.append(users['@odata.id'])
    for uri in allusers:
        response = self.get_request((self.root_uri + uri))
        if (response['ret'] is False):
            return response
        data = response['data']
        if (not (data['UserName'] == '')):
            allusers_details.append(dict(Id=data['Id'], Name=data['Name'], UserName=data['UserName'], RoleId=data['RoleId']))
    result['entries'] = allusers_details
    return result