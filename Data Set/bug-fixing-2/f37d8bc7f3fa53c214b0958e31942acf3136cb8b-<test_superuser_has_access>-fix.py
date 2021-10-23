

def test_superuser_has_access(self):
    self.login_as(user=self.superuser, superuser=True)
    response = self.client.get(self.url, format='json')
    assert (response.status_code == 200)
    assert ({
        'id': self.app_2.id,
        'slug': self.app_2.slug,
        'name': self.app_2.name,
        'installs': 1,
    } in json.loads(response.content))
    assert ({
        'id': self.app_1.id,
        'slug': self.app_1.slug,
        'name': self.app_1.name,
        'installs': 1,
    } in json.loads(response.content))
