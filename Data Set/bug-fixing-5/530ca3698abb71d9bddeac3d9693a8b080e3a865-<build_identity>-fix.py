def build_identity(self, state):
    data = state['data']
    try:
        id_token = data['id_token']
    except KeyError:
        raise IdentityNotValid(('Missing id_token in OAuth response: %s' % data))
    try:
        (_, payload, _) = map(urlsafe_b64decode, id_token.split('.', 2))
    except Exception as exc:
        raise IdentityNotValid(('Unable to decode id_token: %s' % exc))
    try:
        user_data = json.loads(payload)
    except ValueError as exc:
        raise IdentityNotValid(('Unable to decode id_token payload: %s' % exc))
    user_id = MigratingIdentityId(id=user_data['sub'], legacy_id=user_data['email'])
    return {
        'type': 'google',
        'id': user_id,
        'email': user_data['email'],
        'email_verified': user_data['email_verified'],
        'name': user_data['email'],
        'domain': user_data.get('hd', DEFAULT_GOOGLE_DOMAIN),
        'scopes': sorted(self.oauth_scopes),
        'data': self.get_oauth_data(data),
    }