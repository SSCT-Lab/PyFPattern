def handle(self, *args, **options):
    realm = self.get_realm(options)
    email = options['email']
    try:
        user_profile = self.get_user(email, realm)
    except CommandError:
        print(("e-mail %s doesn't exist in the realm %s, skipping" % (email, realm)))
        return
    fix(user_profile)