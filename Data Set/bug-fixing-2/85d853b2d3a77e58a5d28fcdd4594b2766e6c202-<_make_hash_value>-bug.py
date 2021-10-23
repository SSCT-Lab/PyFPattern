

def _make_hash_value(self, user, timestamp):
    login_timestamp = ('' if (user.last_login is None) else user.last_login.replace(microsecond=0, tzinfo=None))
    return (((str(user.pk) + user.password) + str(login_timestamp)) + str(timestamp))
