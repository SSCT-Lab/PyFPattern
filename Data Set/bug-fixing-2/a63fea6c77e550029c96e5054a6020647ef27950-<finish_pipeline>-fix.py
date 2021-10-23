

def finish_pipeline(self):
    data = self.fetch_state()
    if (not data):
        return self.error(ERR_INVALID_IDENTITY)
    try:
        identity = self.provider.build_identity(data)
    except IdentityNotValid:
        return self.error(ERR_INVALID_IDENTITY)
    if (self.state.flow == self.FLOW_LOGIN):
        response = self._finish_login_pipeline(identity)
    elif (self.state.flow == self.FLOW_SETUP_PROVIDER):
        response = self._finish_setup_pipeline(identity)
    return response
