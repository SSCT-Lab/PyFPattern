

def gather_facts(self):
    current_path = os.path.join(self.path, self.current_path)
    releases_path = os.path.join(self.path, self.releases_path)
    if self.shared_path:
        shared_path = os.path.join(self.path, self.shared_path)
    else:
        shared_path = None
    (previous_release, previous_release_path) = self._get_last_release(current_path)
    if ((not self.release) and ((self.state == 'query') or (self.state == 'present'))):
        self.release = time.strftime('%Y%m%d%H%M%S')
    if self.release:
        new_release_path = os.path.join(releases_path, self.release)
    else:
        new_release_path = None
    return {
        'project_path': self.path,
        'current_path': current_path,
        'releases_path': releases_path,
        'shared_path': shared_path,
        'previous_release': previous_release,
        'previous_release_path': previous_release_path,
        'new_release': self.release,
        'new_release_path': new_release_path,
        'unfinished_filename': self.unfinished_filename,
    }
