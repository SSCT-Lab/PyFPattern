@g_connect
def create_import_task(self, github_user, github_repo, reference=None, role_name=None):
    '\n        Post an import request\n        '
    url = ('%s/imports/' % self.baseurl)
    args = {
        'github_user': github_user,
        'github_repo': github_repo,
        'github_reference': (reference if reference else ''),
    }
    if role_name:
        args['alternate_role_name'] = role_name
    elif github_repo.startswith('ansible-role'):
        args['alternate_role_name'] = github_repo[(len('ansible-role') + 1):]
    data = self.__call_galaxy(url, args=urlencode(args), method='POST')
    if data.get('results', None):
        return data['results']
    return data