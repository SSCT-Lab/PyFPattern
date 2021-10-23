def _get_credentials(self):
    '\n        Returns the Credentials object for Google API\n        '
    key_path = self._get_field('key_path', False)
    keyfile_dict = self._get_field('keyfile_dict', False)
    scope = self._get_field('scope', None)
    if scope:
        scopes = [s.strip() for s in scope.split(',')]
    else:
        scopes = _DEFAULT_SCOPES
    if ((not key_path) and (not keyfile_dict)):
        self.log.info('Getting connection using `google.auth.default()` since no key file is defined for hook.')
        (credentials, _) = google.auth.default(scopes=scopes)
    elif key_path:
        if key_path.endswith('.json'):
            self.log.debug(('Getting connection using JSON key file %s' % key_path))
            credentials = google.oauth2.service_account.Credentials.from_service_account_file(key_path, scopes=scopes)
        elif key_path.endswith('.p12'):
            raise AirflowException('Legacy P12 key file are not supported, use a JSON key file.')
        else:
            raise AirflowException('Unrecognised extension for key file.')
    else:
        try:
            keyfile_dict = json.loads(keyfile_dict)
            keyfile_dict['private_key'] = keyfile_dict['private_key'].replace('\\n', '\n')
            credentials = google.oauth2.service_account.Credentials.from_service_account_info(keyfile_dict, scopes=scopes)
        except json.decoder.JSONDecodeError:
            raise AirflowException('Invalid key JSON.')
    return (credentials.with_subject(self.delegate_to) if self.delegate_to else credentials)