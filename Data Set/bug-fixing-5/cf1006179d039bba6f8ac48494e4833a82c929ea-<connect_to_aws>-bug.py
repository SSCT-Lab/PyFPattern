def connect_to_aws(self, module, region):
    connect_args = self.credentials
    if self.boto_profile:
        connect_args['profile_name'] = self.boto_profile
        self.boto_fix_security_token_in_profile(connect_args)
    if self.iam_role:
        sts_conn = sts.connect_to_region(region, **connect_args)
        role = sts_conn.assume_role(self.iam_role, 'ansible_dynamic_inventory')
        connect_args['aws_access_key_id'] = role.credentials.access_key
        connect_args['aws_secret_access_key'] = role.credentials.secret_key
        connect_args['security_token'] = role.credentials.session_token
    conn = module.connect_to_region(region, **connect_args)
    if (conn is None):
        self.fail_with_error(('region name: %s likely not supported, or AWS is down.  connection to region failed.' % region))
    return conn