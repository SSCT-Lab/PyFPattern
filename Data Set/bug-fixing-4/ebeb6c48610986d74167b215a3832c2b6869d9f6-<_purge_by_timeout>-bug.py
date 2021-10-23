@staticmethod
def _purge_by_timeout(dt):
    curtime = Clock.get_time()
    for category in Cache._objects:
        if (category not in Cache._categories):
            continue
        timeout = Cache._categories[category]['timeout']
        if ((timeout is not None) and (dt > timeout)):
            timeout *= 2
            Cache._categories[category]['timeout'] = timeout
            continue
        for key in list(Cache._objects[category].keys())[:]:
            lastaccess = Cache._objects[category][key]['lastaccess']
            objtimeout = Cache._objects[category][key]['timeout']
            if (objtimeout is not None):
                timeout = objtimeout
            if (timeout is None):
                continue
            if ((curtime - lastaccess) > timeout):
                del Cache._objects[category][key]