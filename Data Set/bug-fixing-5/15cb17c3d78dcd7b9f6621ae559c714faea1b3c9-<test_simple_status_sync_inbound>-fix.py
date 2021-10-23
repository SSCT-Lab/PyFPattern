@patch.object(IssueSyncMixin, 'sync_status_inbound')
def test_simple_status_sync_inbound(self, mock_sync_status_inbound):
    org = self.organization
    integration = Integration.objects.create(provider='jira', name='Example Jira')
    integration.add_organization(org.id)
    path = reverse('sentry-extensions-jira-issue-updated')
    with patch('sentry.integrations.jira.webhooks.get_integration_from_jwt', return_value=integration) as mock_get_integration_from_jwt:
        resp = self.client.post(path, data=json.loads(SAMPLE_EDIT_ISSUE_PAYLOAD_STATUS.strip()), HTTP_AUTHORIZATION='JWT anexampletoken')
        assert (resp.status_code == 200)
        mock_get_integration_from_jwt.assert_called_with('anexampletoken', '/extensions/jira/issue-updated/', 'jira', {
            
        }, method='POST')
        mock_sync_status_inbound.assert_called_with('APP-123', {
            'changelog': {
                'from': '10101',
                'field': 'status',
                'fromString': 'Done',
                'to': '3',
                'toString': 'In Progress',
                'fieldtype': 'jira',
                'fieldId': 'status',
            },
            'issue': {
                'fields': {
                    'project': {
                        'id': '10000',
                        'key': 'APP',
                    },
                },
                'key': 'APP-123',
            },
        })