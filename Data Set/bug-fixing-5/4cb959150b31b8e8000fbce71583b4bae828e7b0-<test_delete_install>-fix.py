@responses.activate
def test_delete_install(self):
    responses.add(url='https://example.com/webhook', method=responses.POST, body={
        
    })
    self.login_as(user=self.user)
    response = self.client.delete(self.url, format='json')
    assert (response.status_code == 204)