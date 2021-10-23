

def run(self, terms, variables=None, boto_profile=None, aws_profile=None, aws_secret_key=None, aws_access_key=None, aws_security_token=None, region=None, bypath=False, shortnames=False, recursive=False, decrypt=True):
    "\n            :arg terms: a list of lookups to run.\n                e.g. ['parameter_name', 'parameter_name_too' ]\n            :kwarg variables: ansible variables active at the time of the lookup\n            :kwarg aws_secret_key: identity of the AWS key to use\n            :kwarg aws_access_key: AWS secret key (matching identity)\n            :kwarg aws_security_token: AWS session key if using STS\n            :kwarg decrypt: Set to True to get decrypted parameters\n            :kwarg region: AWS region in which to do the lookup\n            :kwarg bypath: Set to True to do a lookup of variables under a path\n            :kwarg recursive: Set to True to recurse below the path (requires bypath=True)\n            :returns: A list of parameter values or a list of dictionaries if bypath=True.\n        "
    if (not HAS_BOTO3):
        raise AnsibleError('botocore and boto3 are required for aws_ssm lookup.')
    ret = []
    response = {
        
    }
    ssm_dict = {
        
    }
    credentials = {
        
    }
    if aws_profile:
        credentials['boto_profile'] = aws_profile
    else:
        credentials['boto_profile'] = boto_profile
    credentials['aws_secret_access_key'] = aws_secret_key
    credentials['aws_access_key_id'] = aws_access_key
    credentials['aws_session_token'] = aws_security_token
    client = _boto3_conn(region, credentials)
    ssm_dict['WithDecryption'] = decrypt
    if bypath:
        ssm_dict['Recursive'] = recursive
        for term in terms:
            ssm_dict['Path'] = term
            display.vvv(('AWS_ssm path lookup term: %s in region: %s' % (term, region)))
            try:
                response = client.get_parameters_by_path(**ssm_dict)
            except ClientError as e:
                raise AnsibleError('SSM lookup exception: {0}'.format(to_native(e)))
            paramlist = list()
            paramlist.extend(response['Parameters'])
            while ('NextToken' in response):
                response = client.get_parameters_by_path(NextToken=response['NextToken'], **ssm_dict)
                paramlist.extend(response['Parameters'])
            if shortnames:
                for x in paramlist:
                    x['Name'] = x['Name'][(x['Name'].rfind('/') + 1):]
            display.vvvv(('AWS_ssm path lookup returned: %s' % str(paramlist)))
            if len(paramlist):
                ret.append(boto3_tag_list_to_ansible_dict(paramlist, tag_name_key_name='Name', tag_value_key_name='Value'))
            else:
                ret.append({
                    
                })
    else:
        display.vvv(('AWS_ssm name lookup term: %s' % terms))
        ssm_dict['Names'] = terms
        try:
            response = client.get_parameters(**ssm_dict)
        except ClientError as e:
            raise AnsibleError('SSM lookup exception: {0}'.format(to_native(e)))
        params = boto3_tag_list_to_ansible_dict(response['Parameters'], tag_name_key_name='Name', tag_value_key_name='Value')
        for i in terms:
            if (i in params):
                ret.append(params[i])
            elif (i in response['InvalidParameters']):
                ret.append(None)
            else:
                raise AnsibleError('Ansible internal error: aws_ssm lookup failed to understand boto3 return value: {0}'.format(str(response)))
        return ret
    display.vvvv(('AWS_ssm path lookup returning: %s ' % str(ret)))
    return ret
