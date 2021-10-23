@property
def json(self):
    if (not self.body):
        if ('body' in self.info):
            return json.loads(to_text(self.info['body'], errors='surrogate_or_strict'))
        return None
    try:
        return json.loads(to_text(self.body, errors='surrogate_or_strict'))
    except ValueError:
        return None