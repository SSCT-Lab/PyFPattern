@transaction.atomic
def _finish_login_pipeline(self, identity):
    "\n        The login flow executes both with anonymous and authenticated users.\n\n        Upon completion a few branches exist:\n\n        If the identity is already linked, the user should be logged in\n        and redirected immediately.\n\n        Otherwise, the user is presented with a confirmation window. That window\n        will show them the new account that will be created, and if they're\n        already authenticated an optional button to associate the identity with\n        their account.\n        "
    auth_provider = self.auth_provider
    lock = locks.get('sso:auth:{}:{}'.format(auth_provider.id, md5(unicode(identity['id'])).hexdigest()), duration=5)
    with TimedRetryPolicy(5)(lock.acquire):
        try:
            auth_identity = AuthIdentity.objects.get(auth_provider=auth_provider, ident=identity['id'])
        except AuthIdentity.DoesNotExist:
            return self._handle_unknown_identity(identity)
        return self._handle_existing_identity(auth_identity, identity)