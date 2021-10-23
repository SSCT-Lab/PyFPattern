def process_dist_files(self):
    dist_file_facts = {
        
    }
    dist_guess = self._guess_distribution()
    dist_file_facts.update(dist_guess)
    for ddict in self.OSDIST_LIST:
        name = ddict['name']
        path = ddict['path']
        allow_empty = ddict.get('allowempty', False)
        (has_dist_file, dist_file_content) = self._get_dist_file_content(path, allow_empty=allow_empty)
        if (has_dist_file and allow_empty):
            dist_file_facts['distribution'] = name
            dist_file_facts['distribution_file_path'] = path
            dist_file_facts['distribution_file_variety'] = name
            break
        if (not has_dist_file):
            continue
        (parsed_dist_file, parsed_dist_file_facts) = self._parse_dist_file(name, dist_file_content, path, dist_file_facts)
        if parsed_dist_file:
            dist_file_facts['distribution'] = name
            dist_file_facts['distribution_file_path'] = path
            dist_file_facts['distribution_file_variety'] = name
            dist_file_facts['distribution_file_parsed'] = parsed_dist_file
            dist_file_facts.update(parsed_dist_file_facts)
            break
    return dist_file_facts