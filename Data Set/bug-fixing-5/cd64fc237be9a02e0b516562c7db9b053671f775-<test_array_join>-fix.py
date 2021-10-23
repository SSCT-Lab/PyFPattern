def test_array_join(self):
    with self.feature('organizations:discover'):
        url = reverse('sentry-api-0-organization-discover', args=[self.org.slug])
        response = self.client.post(url, {
            'projects': [self.project.id],
            'fields': ['message', 'exception_stacks.type'],
            'start': (datetime.now() - timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S'),
            'end': (datetime.now() + timedelta(seconds=10)).strftime('%Y-%m-%dT%H:%M:%S'),
            'orderby': '-timestamp',
        })
    assert (response.status_code == 200), response.content
    assert (len(response.data['data']) == 1)
    assert (response.data['data'][0]['exception_stacks.type'] == 'ValidationError')