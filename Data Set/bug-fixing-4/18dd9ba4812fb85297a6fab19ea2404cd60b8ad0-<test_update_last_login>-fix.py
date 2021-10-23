def test_update_last_login(self):
    'Only `last_login` is updated in `update_last_login`'
    user = self.u3
    old_last_login = user.last_login
    user.username = "This username shouldn't get saved"
    request = RequestFactory().get('/login')
    signals.user_logged_in.send(sender=user.__class__, request=request, user=user)
    user = User.objects.get(pk=user.pk)
    self.assertEqual(user.username, 'staff')
    self.assertNotEqual(user.last_login, old_last_login)