def setUp(self):
    super(OrganizationDiscoverTest, self).setUp()
    self.login_as(user=self.user, superuser=False)
    self.org = self.create_organization(owner=self.user, name='foo')
    self.project = self.create_project(organization=self.org, name='Bengal')
    sec_ago = (datetime.utcnow() - timedelta(seconds=1)).isoformat()[:19]
    self.event = self.store_event(data={
        'event_id': ('a' * 32),
        'platform': 'python',
        'environment': 'staging',
        'fingerprint': ['group_1'],
        'message': 'message!',
        'tags': {
            'sentry:release': 'foo',
        },
        'exception': {
            'values': [{
                'type': 'ValidationError',
                'value': 'Bad request',
                'mechanism': {
                    'type': '1',
                    'value': '1',
                },
                'stacktrace': {
                    'frames': [{
                        'function': '?',
                        'filename': 'http://localhost:1337/error.js',
                        'lineno': 29,
                        'colno': 3,
                        'in_app': False,
                    }],
                },
            }],
        },
        'timestamp': sec_ago,
    }, project_id=self.project.id)
    self.path = '/organizations/{}/discover/'.format(self.org.slug)