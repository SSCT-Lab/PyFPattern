def get_sdk_urls():
    try:
        rv = settings.SDK_URLS
        rv.update(((key, info['docs_url']) for (key, info) in get_sdk_versions()))
        return rv
    except Exception:
        logger.exception('sentry-release-registry.sdk-urls')
        return {
            
        }