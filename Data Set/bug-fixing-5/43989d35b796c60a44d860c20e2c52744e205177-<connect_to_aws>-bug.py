def connect_to_aws(aws_module, region, **params):
    conn = aws_module.connect_to_region(region, **params)
    if (not conn):
        if (region not in [aws_module_region.name for aws_module_region in aws_module.regions()]):
            raise AnsibleAWSError(('Region %s does not seem to be available for aws module %s. If the region definitely exists, you may need to upgrade boto or extend with endpoints_path' % (region, aws_module.__name__)))
        else:
            raise AnsibleAWSError(('Unknown problem connecting to region %s for aws module %s.' % (region, aws_module.__name__)))
    if params.get('profile_name'):
        conn = boto_fix_security_token_in_profile(conn, params['profile_name'])
    return conn