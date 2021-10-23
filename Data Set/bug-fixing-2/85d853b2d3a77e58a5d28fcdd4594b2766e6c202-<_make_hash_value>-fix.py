

def _make_hash_value(self, user, timestamp):
    "\n        Hash the user's primary key and some user state that's sure to change\n        after a password reset to produce a token that invalidated when it's\n        used:\n        1. The password field will change upon a password reset (even if the\n           same password is chosen, due to password salting).\n        2. The last_login field will usually be updated very shortly after\n           a password reset.\n        Failing those things, settings.PASSWORD_RESET_TIMEOUT_DAYS eventually\n        invalidates the token.\n\n        Running this data through salted_hmac() prevents password cracking\n        attempts using the reset token, provided the secret isn't compromised.\n        "
    login_timestamp = ('' if (user.last_login is None) else user.last_login.replace(microsecond=0, tzinfo=None))
    return (((str(user.pk) + user.password) + str(login_timestamp)) + str(timestamp))
