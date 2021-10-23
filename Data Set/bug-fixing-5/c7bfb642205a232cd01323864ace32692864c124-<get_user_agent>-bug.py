def get_user_agent(self, data):
    try:
        for (key, value) in data['request']['headers']:
            if (key.lower() == 'user-agent'):
                return value
    except LookupError:
        return ''