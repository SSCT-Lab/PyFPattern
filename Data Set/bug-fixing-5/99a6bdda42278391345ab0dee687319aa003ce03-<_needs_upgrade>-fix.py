def _needs_upgrade():
    version_configured = options.get('sentry:version-configured')
    if (not version_configured):
        return True
    smtp_disabled = (not is_smtp_enabled())
    for key in options.filter(flag=options.FLAG_REQUIRED):
        if (key.flags & options.FLAG_ALLOW_EMPTY):
            continue
        if (smtp_disabled and (key.name[:5] == 'mail.')):
            continue
        if (not options.isset(key.name)):
            return True
    if (version_configured != sentry.get_version()):
        options.set('sentry:version-configured', sentry.get_version())
    return False