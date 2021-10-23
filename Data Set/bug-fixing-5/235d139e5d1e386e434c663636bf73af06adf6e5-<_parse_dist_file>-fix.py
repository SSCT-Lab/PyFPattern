def _parse_dist_file(self, name, dist_file_content, path, collected_facts):
    dist_file_dict = {
        
    }
    if (name in self.SEARCH_STRING):
        if (self.SEARCH_STRING[name] in dist_file_content):
            dist_file_dict['distribution'] = name
        else:
            dist_file_dict['distribution'] = dist_file_content.split()[0]
        return (True, dist_file_dict)
    if (name in self.OS_RELEASE_ALIAS):
        if (self.OS_RELEASE_ALIAS[name] in dist_file_content):
            dist_file_dict['distribution'] = name
            return (True, dist_file_dict)
        return (False, dist_file_dict)
    try:
        distfunc_name = ('parse_distribution_file_' + name)
        distfunc = getattr(self, distfunc_name)
        (parsed, dist_file_dict) = distfunc(name, dist_file_content, path, collected_facts)
        return (parsed, dist_file_dict)
    except AttributeError as exc:
        print(('exc: %s' % exc))
        return (False, dist_file_dict)
    return (True, dist_file_dict)