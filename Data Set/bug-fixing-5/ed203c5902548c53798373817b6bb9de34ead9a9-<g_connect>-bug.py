def g_connect(versions):
    '\n    Wrapper to lazily initialize connection info to Galaxy and verify the API versions required are available on the\n    endpoint.\n\n    :param versions: A list of API versions that the function supports.\n    '

    def decorator(method):

        def wrapped(self, *args, **kwargs):
            if (not self._available_api_versions):
                display.vvvv(('Initial connection to galaxy_server: %s' % self.api_server))
                n_url = self.api_server
                error_context_msg = ('Error when finding available api versions from %s (%s)' % (self.name, n_url))
                if ((self.api_server == 'https://galaxy.ansible.com') or (self.api_server == 'https://galaxy.ansible.com/')):
                    n_url = 'https://galaxy.ansible.com/api/'
                try:
                    data = self._call_galaxy(n_url, method='GET', error_context_msg=error_context_msg)
                except (AnsibleError, GalaxyError, ValueError, KeyError):
                    n_url = _urljoin(n_url, '/api/')
                    data = self._call_galaxy(n_url, method='GET', error_context_msg=error_context_msg)
                    if ('available_versions' not in data):
                        raise AnsibleError(("Tried to find galaxy API root at %s but no 'available_versions' are available on %s" % (n_url, self.api_server)))
                available_versions = data.get('available_versions', {
                    'v1': 'v1/',
                })
                if (list(available_versions.keys()) == ['v1']):
                    available_versions['v2'] = 'v2/'
                self._available_api_versions = available_versions
                display.vvvv(("Found API version '%s' with Galaxy server %s (%s)" % (', '.join(available_versions.keys()), self.name, self.api_server)))
            available_versions = set(self._available_api_versions.keys())
            common_versions = set(versions).intersection(available_versions)
            if (not common_versions):
                raise AnsibleError(("Galaxy action %s requires API versions '%s' but only '%s' are available on %s %s" % (method.__name__, ', '.join(versions), ', '.join(available_versions), self.name, self.api_server)))
            return method(self, *args, **kwargs)
        return wrapped
    return decorator