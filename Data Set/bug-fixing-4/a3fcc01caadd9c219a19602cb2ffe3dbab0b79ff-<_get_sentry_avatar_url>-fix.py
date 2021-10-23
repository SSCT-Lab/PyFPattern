def _get_sentry_avatar_url(self):
    url = '/images/sentry-email-avatar.png'
    return absolute_uri(get_asset_url('sentry', url))