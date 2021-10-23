def get_fingerprinting_config_for_project(project):
    from sentry.grouping.fingerprinting import FingerprintingRules, InvalidFingerprintingConfig
    rules = project.get_option('sentry:fingerprint_rules')
    if (not rules):
        return FingerprintingRules([])
    from sentry.utils.cache import cache
    from sentry.utils.hashlib import md5_text
    cache_key = ('fingerprinting-rules:' + md5_text(rules).hexdigest())
    rv = cache.get(cache_key)
    if (rv is not None):
        return FingerprintingRules.from_json(rv)
    try:
        rv = FingerprintingRules.from_config_string((rules or ''))
    except InvalidFingerprintingConfig:
        rv = FingerprintingRules([])
    cache.set(cache_key, rv.to_json())
    return rv