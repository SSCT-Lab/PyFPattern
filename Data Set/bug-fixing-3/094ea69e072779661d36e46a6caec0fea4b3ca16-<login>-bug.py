def login(request, user, backend=None):
    "\n    Persist a user id and a backend in the request. This way a user doesn't\n    have to reauthenticate on every request. Note that data set during\n    the anonymous session is retained when the user logs in.\n    "
    session_auth_hash = ''
    if (user is None):
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()
    if (SESSION_KEY in request.session):
        if ((_get_user_session_key(request) != user.pk) or (session_auth_hash and (request.session.get(HASH_SESSION_KEY) != session_auth_hash))):
            request.session.flush()
    else:
        request.session.cycle_key()
    try:
        backend = (backend or user.backend)
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if (len(backends) == 1):
            (_, backend) = backends[0]
        else:
            raise ValueError('You have multiple authentication backends configured and therefore must provide the `backend` argument or set the `backend` attribute on the user.')
    request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
    request.session[BACKEND_SESSION_KEY] = backend
    request.session[HASH_SESSION_KEY] = session_auth_hash
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)