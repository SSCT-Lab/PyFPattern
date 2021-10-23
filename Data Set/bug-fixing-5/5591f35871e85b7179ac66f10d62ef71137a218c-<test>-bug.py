def test(self):
    url = reverse('sentry-api-0-organization-discover', args=[self.org.slug])
    response = self.client.post(url, {
        'projects': [self.project.id],
        'fields': ['message', 'platform'],
        'start': (datetime.now() - timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S'),
        'end': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'orderby': '-timestamp',
    })
    assert (response.status_code == 200), response.content
    assert (len(response.data['data']) == 1)
    assert (response.data['data'][0]['message'] == 'message!')
    assert (response.data['data'][0]['platform'] == 'python')