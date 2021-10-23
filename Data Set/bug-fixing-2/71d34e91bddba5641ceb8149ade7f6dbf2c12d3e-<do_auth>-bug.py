

def do_auth(self, *args, **kwargs):
    kwargs['return_data'] = {
        
    }
    request = self.strategy.request
    kwargs['realm_subdomain'] = get_subdomain(request)
    user_profile = None
    team_id = settings.SOCIAL_AUTH_GITHUB_TEAM_ID
    org_name = settings.SOCIAL_AUTH_GITHUB_ORG_NAME
    if ((team_id is None) and (org_name is None)):
        user_profile = GithubOAuth2.do_auth(self, *args, **kwargs)
    elif team_id:
        backend = GithubTeamOAuth2(self.strategy, self.redirect_uri)
        try:
            user_profile = backend.do_auth(*args, **kwargs)
        except AuthFailed:
            logging.info('User profile not member of team.')
            user_profile = None
    elif org_name:
        backend = GithubOrganizationOAuth2(self.strategy, self.redirect_uri)
        try:
            user_profile = backend.do_auth(*args, **kwargs)
        except AuthFailed:
            logging.info('User profile not member of organisation.')
            user_profile = None
    return self.process_do_auth(user_profile, *args, **kwargs)
