def get_gce_driver(self):
    'Determine the GCE authorization settings and return a\n        libcloud driver.\n        '
    secrets_path = self.config.get('gce', 'libcloud_secrets')
    secrets_found = False
    try:
        import secrets
        args = list(secrets.GCE_PARAMS)
        kwargs = secrets.GCE_KEYWORD_PARAMS
        secrets_found = True
    except:
        pass
    if ((not secrets_found) and secrets_path):
        if (not secrets_path.endswith('secrets.py')):
            err = 'Must specify libcloud secrets file as '
            err += '/absolute/path/to/secrets.py'
            sys.exit(err)
        sys.path.append(os.path.dirname(secrets_path))
        try:
            import secrets
            args = list(getattr(secrets, 'GCE_PARAMS', []))
            kwargs = getattr(secrets, 'GCE_KEYWORD_PARAMS', {
                
            })
            secrets_found = True
        except:
            pass
    if (not secrets_found):
        args = [self.config.get('gce', 'gce_service_account_email_address'), self.config.get('gce', 'gce_service_account_pem_file_path')]
        kwargs = {
            'project': self.config.get('gce', 'gce_project_id'),
            'datacenter': self.config.get('gce', 'gce_zone'),
        }
    args[0] = os.environ.get('GCE_EMAIL', args[0])
    args[1] = os.environ.get('GCE_PEM_FILE_PATH', args[1])
    kwargs['project'] = os.environ.get('GCE_PROJECT', kwargs['project'])
    kwargs['datacenter'] = os.environ.get('GCE_ZONE', kwargs['datacenter'])
    gce = get_driver(Provider.GCE)(*args, **kwargs)
    gce.connection.user_agent_append(('%s/%s' % (USER_AGENT_PRODUCT, USER_AGENT_VERSION)))
    return gce