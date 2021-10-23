

@property
def repos_urls(self):
    _repositories = []
    for parsed_repos in self.files.values():
        for parsed_repo in parsed_repos:
            valid = parsed_repo[1]
            enabled = parsed_repo[2]
            source_line = parsed_repo[3]
            if ((not valid) or (not enabled)):
                continue
            if source_line.startswith('ppa:'):
                (source, ppa_owner, ppa_name) = self._expand_ppa(source_line)
                _repositories.append(source)
            else:
                _repositories.append(source_line)
    return _repositories
