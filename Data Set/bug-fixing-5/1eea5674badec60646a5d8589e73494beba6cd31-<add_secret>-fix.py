@g_connect
def add_secret(self, source, github_user, github_repo, secret):
    url = ('%s/notification_secrets/' % self.baseurl)
    args = urlencode({
        'source': source,
        'github_user': github_user,
        'github_repo': github_repo,
        'secret': secret,
    })
    data = self.__call_galaxy(url, args=args, method='POST')
    return data