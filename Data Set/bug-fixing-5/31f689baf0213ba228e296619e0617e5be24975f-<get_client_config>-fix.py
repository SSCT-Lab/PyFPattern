def get_client_config(request=None):
    '\n    Provides initial bootstrap data needed to boot the frontend application.\n    '
    if (request is not None):
        user = (getattr(request, 'user', None) or AnonymousUser())
        messages = get_messages(request)
        session = getattr(request, 'session', None)
        is_superuser = is_active_superuser(request)
        language_code = getattr(request, 'LANGUAGE_CODE', 'en')
        user_identity = {
            'ip_address': request.META['REMOTE_ADDR'],
        }
        if (user and user.is_authenticated()):
            user_identity.update({
                'email': user.email,
                'id': user.id,
            })
            if user.name:
                user_identity['name'] = user.name
    else:
        user = None
        user_identity = {
            
        }
        messages = []
        is_superuser = False
        language_code = 'en'
    enabled_features = []
    if features.has('organizations:create', actor=user):
        enabled_features.append('organizations:create')
    if auth.has_user_registration():
        enabled_features.append('auth:register')
    version_info = _get_version_info()
    needs_upgrade = False
    if is_superuser:
        needs_upgrade = _needs_upgrade()
    public_dsn = _get_public_dsn()
    context = {
        'singleOrganization': settings.SENTRY_SINGLE_ORGANIZATION,
        'supportEmail': get_support_mail(),
        'urlPrefix': options.get('system.url-prefix'),
        'version': version_info,
        'features': enabled_features,
        'distPrefix': get_asset_url('sentry', 'dist/'),
        'needsUpgrade': needs_upgrade,
        'dsn': public_dsn,
        'statuspage': _get_statuspage(),
        'messages': [{
            'message': msg.message,
            'level': msg.tags,
        } for msg in messages],
        'isOnPremise': settings.SENTRY_ONPREMISE,
        'invitesEnabled': settings.SENTRY_ENABLE_INVITES,
        'gravatarBaseUrl': settings.SENTRY_GRAVATAR_BASE_URL,
        'termsUrl': settings.TERMS_URL,
        'privacyUrl': settings.PRIVACY_URL,
        'lastOrganization': (session['activeorg'] if (session and ('activeorg' in session)) else None),
        'languageCode': language_code,
        'userIdentity': user_identity,
        'csrfCookieName': settings.CSRF_COOKIE_NAME,
        'sentryConfig': {
            'dsn': public_dsn,
            'release': version_info['build'],
            'whitelistUrls': list(('' if (settings.ALLOWED_HOSTS == ['*']) else settings.ALLOWED_HOSTS)),
        },
    }
    if (user and user.is_authenticated()):
        context.update({
            'isAuthenticated': True,
            'user': serialize(user, user, DetailedUserSerializer()),
        })
        if request.user.is_superuser:
            context['user']['isSuperuser'] = request.user.is_superuser
    else:
        context.update({
            'isAuthenticated': False,
            'user': None,
        })
    return context