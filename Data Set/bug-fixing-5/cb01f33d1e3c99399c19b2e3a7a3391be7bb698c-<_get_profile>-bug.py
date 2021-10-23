def _get_profile(self, profile='default'):
    path = expanduser('~')
    path += '/.azure/credentials'
    try:
        config = ConfigParser.ConfigParser()
        config.read(path)
    except Exception as exc:
        self.fail('Failed to access {0}. Check that the file exists and you have read access. {1}'.format(path, str(exc)))
    credentials = dict()
    for key in AZURE_CREDENTIAL_ENV_MAPPING:
        try:
            credentials[key] = config.get(profile, key, raw=True)
        except:
            pass
    if ((credentials.get('client_id') is not None) or (credentials.get('ad_user') is not None)):
        return credentials
    return None