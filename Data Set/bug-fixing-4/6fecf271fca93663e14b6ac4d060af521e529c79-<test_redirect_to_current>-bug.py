def test_redirect_to_current(self):
    '\n        Should redirect to the setting for the current site taken from the URL,\n        by default\n        '
    start_url = reverse('wagtailsettings:edit', args=['tests', 'testsetting'])
    dest_url = ('http://example.com' + reverse('wagtailsettings:edit', args=['tests', 'testsetting', self.other_site.pk]))
    response = self.client.get(start_url, follow=True, HTTP_HOST=self.other_site.hostname)
    self.assertRedirects(response, dest_url, status_code=302, fetch_redirect_response=False)