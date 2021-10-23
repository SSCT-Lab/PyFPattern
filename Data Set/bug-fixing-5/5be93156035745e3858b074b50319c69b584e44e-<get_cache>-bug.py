def get_cache(module):
    'Attempt to get the cache object and update till it works'
    cache = None
    try:
        cache = apt.Cache()
    except SystemError as e:
        if ('/var/lib/apt/lists/' in to_native(e).lower()):
            retries = 0
            while (retries < 2):
                (rc, so, se) = module.run_command(['apt-get', 'update', '-q'])
                retries += 1
                if (rc == 0):
                    break
            if (rc != 0):
                module.fail_json(msg=('Updating the cache to correct corrupt package lists failed:\n%s\n%s' % (to_native(e), (so + se))), rc=rc)
            cache = apt.Cache()
        else:
            module.fail_json(msg=str(e))
    return cache