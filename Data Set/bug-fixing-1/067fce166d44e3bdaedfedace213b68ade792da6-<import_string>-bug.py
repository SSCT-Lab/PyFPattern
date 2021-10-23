

def import_string(path):
    "\n    Path must be module.path.ClassName\n\n    >>> cls = import_string('sentry.models.Group')\n    "
    result = _cache[path]
    return result
