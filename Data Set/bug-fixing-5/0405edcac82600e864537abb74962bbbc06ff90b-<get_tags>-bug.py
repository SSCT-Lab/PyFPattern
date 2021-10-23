def get_tags(self, **kwargs):
    '\n         Returns tag list for selected instance of EFS\n        '
    tags = iterate_all('Tags', self.connection.describe_tags, **kwargs)
    return dict(((tag['Key'], tag['Value']) for tag in tags))