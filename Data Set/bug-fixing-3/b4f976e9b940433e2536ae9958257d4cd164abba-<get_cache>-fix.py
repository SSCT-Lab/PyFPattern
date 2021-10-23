def get_cache(module):
    'Attempt to get the cache object and update till it works'
    cache = None
    try:
        cache = apt.Cache()
    except SystemError:
        e = get_exception()
        if ('/var/lib/apt/lists/' in str(e).lower()):
            retries = 0
            while (retries < 2):
                (rc, so, se) = module.run_command(['apt-get', 'update', '-q'])
                retries += 1
                if (rc == 0):
                    break
            if (rc != 0):
                module.fail_json(msg=('Updating the cache to correct corrupt package lists failed:\n%s\n%s' % (str(e), (str(so) + str(se)))), rc=rc)
            cache = apt.Cache()
        else:
            module.fail_json(msg=str(e))
    return cache