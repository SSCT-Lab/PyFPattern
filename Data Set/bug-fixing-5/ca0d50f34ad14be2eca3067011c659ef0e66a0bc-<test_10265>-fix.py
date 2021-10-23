def test_10265(self):
    '\n        The token generated for a user created in the same request\n        will work correctly.\n        '
    user = User.objects.create_user('comebackkid', 'test3@example.com', 'testpw')
    user_reload = User.objects.get(username='comebackkid')
    p0 = MockedPasswordResetTokenGenerator(datetime.now())
    tk1 = p0.make_token(user)
    tk2 = p0.make_token(user_reload)
    self.assertEqual(tk1, tk2)