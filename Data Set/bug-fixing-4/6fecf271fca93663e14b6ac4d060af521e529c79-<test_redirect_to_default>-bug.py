def test_redirect_to_default(self):
    '\n        Should redirect to the setting for the default site.\n        '
    start_url = reverse('wagtailsettings:edit', args=['tests', 'testsetting'])
    dest_url = ('http://testserver' + reverse('wagtailsettings:edit', args=['tests', 'testsetting', self.default_site.pk]))
    response = self.client.get(start_url, follow=True)
    self.assertRedirects(response, dest_url, status_code=302, fetch_redirect_response=False)