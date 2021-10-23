def get_app_url(self):
    name = options.get('github-app.name')
    return ('https://github.com/apps/%s' % slugify(name))