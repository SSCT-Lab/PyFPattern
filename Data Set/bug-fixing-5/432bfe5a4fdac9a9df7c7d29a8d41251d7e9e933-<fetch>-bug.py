def fetch(self, role_data):
    '\n        Downloads the archived role from github to a temp location\n        '
    if role_data:
        if (('github_user' in role_data) and ('github_repo' in role_data)):
            archive_url = ('https://github.com/%s/%s/archive/%s.tar.gz' % (role_data['github_user'], role_data['github_repo'], self.version))
        else:
            archive_url = self.src
        display.display(('- downloading role from %s' % archive_url))
        try:
            url_file = open_url(archive_url)
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            data = url_file.read()
            while data:
                temp_file.write(data)
                data = url_file.read()
            temp_file.close()
            return temp_file.name
        except Exception as e:
            display.error(('failed to download the file: %s' % str(e)))
    return False