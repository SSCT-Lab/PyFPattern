def setup():
    default_creds_file = os.path.expanduser('~/.rackspace_cloud_credentials')
    env = get_config(p, 'rax', 'environment', 'RAX_ENV', None)
    if env:
        pyrax.set_environment(env)
    keyring_username = pyrax.get_setting('keyring_username')
    creds_file = get_config(p, 'rax', 'creds_file', 'RAX_CREDS_FILE', None)
    if (creds_file is not None):
        creds_file = os.path.expanduser(creds_file)
    elif os.path.isfile(default_creds_file):
        creds_file = default_creds_file
    elif (not keyring_username):
        sys.exit(('No value in environment variable %s and/or no credentials file at %s' % ('RAX_CREDS_FILE', default_creds_file)))
    identity_type = pyrax.get_setting('identity_type')
    pyrax.set_setting('identity_type', (identity_type or 'rackspace'))
    region = pyrax.get_setting('region')
    try:
        if keyring_username:
            pyrax.keyring_auth(keyring_username, region=region)
        else:
            pyrax.set_credential_file(creds_file, region=region)
    except Exception as e:
        sys.exit(('%s: %s' % (e, e.message)))
    regions = []
    if region:
        regions.append(region)
    else:
        region_list = get_config(p, 'rax', 'regions', 'RAX_REGION', 'all', islist=True)
        for region in region_list:
            region = region.strip().upper()
            if (region == 'ALL'):
                regions = pyrax.regions
                break
            elif (region not in pyrax.regions):
                sys.exit(('Unsupported region %s' % region))
            elif (region not in regions):
                regions.append(region)
    return regions