def logout(self):
    if hasattr(self, 'login_handle'):
        self.login_handle.logout()
        return True
    return False