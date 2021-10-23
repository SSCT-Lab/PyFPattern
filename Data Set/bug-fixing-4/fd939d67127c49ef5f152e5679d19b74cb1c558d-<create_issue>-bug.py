def create_issue(self, data, **kwargs):
    client = self.get_client()
    issue = client.create_issue(data.get('repo'), data)
    return {
        'key': issue['id'],
        'title': issue['title'],
        'description': issue['content']['html'],
    }