def test_10265(self):
    '\n        The token generated for a user created in the same request\n        will work correctly.\n        '
    user = User.objects.create_user('comebackkid', 'test3@example.com', 'testpw')
    p0 = PasswordResetTokenGenerator()
    tk1 = p0.make_token(user)
    reload = User.objects.get(username='comebackkid')
    tk2 = p0.make_token(reload)
    self.assertEqual(tk1, tk2)