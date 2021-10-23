def match_groups(self, server_info, tags):
    server_zone = extract_zone(server_info=server_info)
    server_tags = extract_tags(server_info=server_info)
    if (server_zone is None):
        return set()
    if (tags is None):
        return set(server_tags).union((server_zone,))
    matching_tags = set(server_tags).intersection(tags)
    if (not matching_tags):
        return set()
    else:
        return matching_tags.union((server_zone,))