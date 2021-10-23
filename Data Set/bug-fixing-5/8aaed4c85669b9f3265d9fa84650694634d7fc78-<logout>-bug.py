def logout(self):
    if self.login_handle:
        self.login_handle.logout()
        return True
    return False