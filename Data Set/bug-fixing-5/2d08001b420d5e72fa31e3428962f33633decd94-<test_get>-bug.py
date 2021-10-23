def test_get(self):
    with self.feature(self.feature_name):
        url = reverse('sentry-api-0-discover-saved-query-detail', args=[self.org.slug, self.query_id])
        response = self.client.get(url)
    assert (response.status_code == 200), response.content
    assert (response.data['id'] == six.text_type(self.query_id))
    assert (response.data['projects'] == self.project_ids)
    assert (response.data['fields'] == ['test'])
    assert (response.data['conditions'] == [])
    assert (response.data['limit'] == 10)