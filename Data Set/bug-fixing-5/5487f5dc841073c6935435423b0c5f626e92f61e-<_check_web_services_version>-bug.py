def _check_web_services_version(self):
    'Verify proxy or embedded web services meets minimum version required for module.\n\n        The minimum required web services version is evaluated against version supplied through the web services rest\n        api. AnsibleFailJson exception will be raised when the minimum is not met or exceeded.\n\n        This helper function will update the supplied api url if secure http is not used for embedded web services\n\n        :raise AnsibleFailJson: raised when the contacted api service does not meet the minimum required version.\n        '
    if (not self.is_web_services_valid_cache):
        url_parts = list(urlparse(self.url))
        if ((not url_parts[0]) or (not url_parts[1])):
            self.module.fail_json(msg=('Failed to provide valid API URL. Example: https://192.168.1.100:8443/devmgr/v2. URL [%s].' % self.url))
        if (url_parts[0] not in ['http', 'https']):
            self.module.fail_json(msg=('Protocol must be http or https. URL [%s].' % self.url))
        self.url = ('%s://%s/' % (url_parts[0], url_parts[1]))
        about_url = (self.url + self.DEFAULT_REST_API_ABOUT_PATH)
        (rc, data) = request(about_url, timeout=self.DEFAULT_TIMEOUT, headers=self.DEFAULT_HEADERS, ignore_errors=True, **self.creds)
        if (rc != 200):
            self.module.warn(('Failed to retrieve web services about information! Retrying with secure ports. Array Id [%s].' % self.ssid))
            self.url = ('https://%s:8443/' % url_parts[1].split(':')[0])
            about_url = (self.url + self.DEFAULT_REST_API_ABOUT_PATH)
            try:
                (rc, data) = request(about_url, timeout=self.DEFAULT_TIMEOUT, headers=self.DEFAULT_HEADERS, **self.creds)
            except Exception as error:
                self.module.fail_json(msg=('Failed to retrieve the webservices about information! Array Id [%s]. Error [%s].' % (self.ssid, to_native(error))))
        (major, minor, other, revision) = data['version'].split('.')
        (minimum_major, minimum_minor, other, minimum_revision) = self.web_services_version.split('.')
        if (not ((major > minimum_major) or ((major == minimum_major) and (minor > minimum_minor)) or ((major == minimum_major) and (minor == minimum_minor) and (revision >= minimum_revision)))):
            self.module.fail_json(msg=('Web services version does not meet minimum version required. Current version: [%s]. Version required: [%s].' % (data['version'], self.web_services_version)))
        self.module.log('Web services rest api version met the minimum required version.')
        self.is_web_services_valid_cache = True