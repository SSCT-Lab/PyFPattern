@property
def json(self):
    if (not self.body):
        if ('body' in self.info):
            return json.loads(self.info['body'])
        return None
    try:
        return json.loads(self.body)
    except ValueError:
        return None