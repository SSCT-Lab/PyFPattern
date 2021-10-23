def get_user_agent(self, data):
    try:
        for (key, value) in (get_path(data, 'request', 'headers', filter=True) or ()):
            if (key.lower() == 'user-agent'):
                return value
    except LookupError:
        return ''