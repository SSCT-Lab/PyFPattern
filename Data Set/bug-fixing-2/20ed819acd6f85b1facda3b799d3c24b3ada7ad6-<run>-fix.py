

def run(self, terms, variables, **kwargs):
    if (not CREDSTASH_INSTALLED):
        raise AnsibleError('The credstash lookup plugin requires credstash to be installed.')
    ret = []
    for term in terms:
        try:
            version = kwargs.pop('version', '')
            region = kwargs.pop('region', None)
            table = kwargs.pop('table', 'credential-store')
            profile_name = kwargs.pop('profile_name', os.getenv('AWS_PROFILE', None))
            aws_access_key_id = kwargs.pop('aws_access_key_id', os.getenv('AWS_ACCESS_KEY_ID', None))
            aws_secret_access_key = kwargs.pop('aws_secret_access_key', os.getenv('AWS_SECRET_ACCESS_KEY', None))
            aws_session_token = kwargs.pop('aws_session_token', os.getenv('AWS_SESSION_TOKEN', None))
            kwargs_pass = {
                'profile_name': profile_name,
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key,
                'aws_session_token': aws_session_token,
            }
            val = credstash.getSecret(term, version, region, table, context=kwargs, **kwargs_pass)
        except credstash.ItemNotFound:
            raise AnsibleError('Key {0} not found'.format(term))
        except Exception as e:
            raise AnsibleError('Encountered exception while fetching {0}: {1}'.format(term, e))
        ret.append(val)
    return ret
