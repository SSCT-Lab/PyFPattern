def test_delete_install(self):
    self.login_as(user=self.user)
    response = self.client.delete(self.url, format='json')
    assert (response.status_code == 204)