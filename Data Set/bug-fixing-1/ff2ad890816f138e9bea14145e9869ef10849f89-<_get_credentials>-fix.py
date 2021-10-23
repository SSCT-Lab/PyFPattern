

def _get_credentials(options):
    credentials = {
        
    }
    credentials['boto_profile'] = options['boto_profile']
    credentials['aws_secret_access_key'] = options['aws_secret_key']
    credentials['aws_access_key_id'] = options['aws_access_key']
    credentials['aws_session_token'] = options['aws_security_token']
    return credentials
