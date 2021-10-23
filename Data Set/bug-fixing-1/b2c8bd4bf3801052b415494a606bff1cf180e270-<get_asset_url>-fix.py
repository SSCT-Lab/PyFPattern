

def get_asset_url(module, path):
    '\n    Returns a versioned asset URL (located within Sentry\'s static files).\n\n    Example:\n      {% asset_url \'sentry\' \'dist/sentry.css\' %}\n      =>  "/_static/74d127b78dc7daf2c51f/sentry/dist/sentry.css"\n    '
    return '{}/{}/{}'.format(settings.STATIC_URL.rstrip('/'), module, path.lstrip('/'))
