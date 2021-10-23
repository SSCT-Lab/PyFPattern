def get(self, request, wizard_hash=None):
    '\n        This tries to retrieve and return the cache content if possible\n        otherwise creates new cache\n        '
    if (wizard_hash is not None):
        key = ('%s%s' % (SETUP_WIZARD_CACHE_KEY, wizard_hash))
        wizard_data = default_cache.get(key)
        if (wizard_data is None):
            return Response(status=404)
        elif (wizard_data == 'empty'):
            return Response(status=400)
        return Response(serialize(wizard_data))
    else:
        rate_limited = ratelimits.is_limited(key=('rl:setup-wizard:ip:%s' % request.META['REMOTE_ADDR']), limit=10)
        if rate_limited:
            logger.info('setup-wizard.rate-limit')
            return Response({'Too many wizard requests'}, status=403)
        wizard_hash = get_random_string(64, allowed_chars='abcdefghijklmnopqrstuvwxyz012345679')
        key = ('%s%s' % (SETUP_WIZARD_CACHE_KEY, wizard_hash))
        default_cache.set(key, 'empty', SETUP_WIZARD_CACHE_TIMEOUT)
        return Response(serialize({
            'hash': wizard_hash,
        }))