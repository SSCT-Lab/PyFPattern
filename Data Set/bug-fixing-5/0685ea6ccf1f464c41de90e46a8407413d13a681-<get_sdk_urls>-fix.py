def get_sdk_urls():
    try:
        rv = dict(settings.SDK_URLS)
        rv.update(((key, info['main_docs_url']) for (key, info) in get_sdk_index().items()))
        return rv
    except Exception:
        logger.exception('sentry-release-registry.sdk-urls')
        return {
            
        }