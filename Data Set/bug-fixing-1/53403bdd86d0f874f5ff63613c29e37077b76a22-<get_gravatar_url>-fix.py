

def get_gravatar_url(email, size=None, default='mm'):
    if (email is None):
        email = ''
    gravatar_url = ('%s/avatar/%s' % (settings.SENTRY_GRAVATAR_BASE_URL, md5(email.lower()).hexdigest()))
    properties = {
        
    }
    if size:
        properties['s'] = str(size)
    if default:
        properties['d'] = default
    if properties:
        gravatar_url += ('?' + urllib.urlencode(properties))
    return gravatar_url
