def get_store(self, key, silent=False):
    "\n        Attempt to fetch value from the database. If successful,\n        also set it back in the cache.\n\n        Returns None in both cases, if the key doesn't actually exist,\n        or if we errored fetching it.\n\n        NOTE: This behavior should probably be improved to differentiate\n        between a miss vs error, but not worth it now since the value\n        is limited at the moment.\n        "
    try:
        value = self.model.objects.get(key=key.name).value
    except (self.model.DoesNotExist, ProgrammingError):
        value = None
    except Exception:
        if (not silent):
            logger.exception('option.failed-lookup', extra={
                'key': key.name,
            })
        value = None
    else:
        try:
            self.set_cache(key, value)
        except Exception:
            if (not silent):
                logger.warn(CACHE_UPDATE_ERR, key.name, extra={
                    'key': key.name,
                }, exc_info=True)
    return value