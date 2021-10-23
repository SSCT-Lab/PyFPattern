def passwd_set(self):
    if (not self.passwd_check()):
        return False
    try:
        self.connection.passwd_set(self.dn, None, self.passwd)
    except ldap.LDAPError as e:
        self.fail('Unable to set password', e)
    return True