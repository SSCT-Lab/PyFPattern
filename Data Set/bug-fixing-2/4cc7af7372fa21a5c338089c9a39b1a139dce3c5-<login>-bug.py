

def login(self):
    '\n        Log into the registry with provided username/password. On success update the config\n        file with the new authorization.\n\n        :return: None\n        '
    if (self.email and (not re.match(EMAIL_REGEX, self.email))):
        self.fail(('Parameter error: the email address appears to be incorrect. Expecting it to match /%s/' % EMAIL_REGEX))
    self.results['actions'].append(('Logged into %s' % self.registry_url))
    self.log(('Log into %s with username %s' % (self.registry_url, self.username)))
    try:
        response = self.client.login(self.username, password=self.password, email=self.email, registry=self.registry_url, reauth=self.reauthorize, dockercfg_path=self.config_path)
    except Exception as exc:
        self.fail(('Logging into %s for user %s failed - %s' % (self.registry_url, self.username, str(exc))))
    self.results['login_result'] = response
    if (not self.check_mode):
        self.update_config_file()
