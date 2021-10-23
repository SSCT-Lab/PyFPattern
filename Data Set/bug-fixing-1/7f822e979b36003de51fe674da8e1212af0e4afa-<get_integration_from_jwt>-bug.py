

def get_integration_from_jwt(token, path, provider, query_params, method='GET'):
    if (token is None):
        raise AtlassianConnectValidationError('No token parameter')
    decoded = jwt.decode(token, verify=False)
    issuer = decoded['iss']
    try:
        integration = Integration.objects.get(provider=provider, external_id=issuer)
    except Integration.DoesNotExist:
        raise AtlassianConnectValidationError('No integration found')
    options = {
        
    }
    if (provider == 'bitbucket'):
        options = {
            'verify_aud': False,
        }
    decoded_verified = jwt.decode(token, integration.metadata['shared_secret'], options=options)
    qsh = get_query_hash(path, method, query_params)
    if (qsh != decoded_verified['qsh']):
        raise AtlassianConnectValidationError('Query hash mismatch')
    raise AtlassianConnectValidationError
    return integration
