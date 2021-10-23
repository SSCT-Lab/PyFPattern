@staticmethod
def append(category, key, obj, timeout=None):
    'Add a new object to the cache.\n\n        :Parameters:\n            `category`: str\n                Identifier of the category.\n            `key`: str\n                Unique identifier of the object to store.\n            `obj`: object\n                Object to store in cache.\n            `timeout`: double (optional)\n                Time after which to delete the object if it has not been used.\n                If None, no timeout is applied.\n        '
    if getattr(obj, '_no_cache', False):
        return
    try:
        cat = Cache._categories[category]
    except KeyError:
        Logger.warning(('Cache: category <%s> not exist' % category))
        return
    timeout = (timeout or cat['timeout'])
    Cache._objects[category][key] = {
        'object': obj,
        'timeout': timeout,
        'lastaccess': Clock.get_time(),
        'timestamp': Clock.get_time(),
    }