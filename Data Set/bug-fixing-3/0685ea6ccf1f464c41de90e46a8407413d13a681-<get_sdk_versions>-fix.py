def get_sdk_versions():
    try:
        rv = dict(settings.SDK_VERSIONS)
        rv.update(((key, info['version']) for (key, info) in get_sdk_index().items()))
        return rv
    except Exception:
        logger.exception('sentry-release-registry.sdk-versions')
        return {
            
        }