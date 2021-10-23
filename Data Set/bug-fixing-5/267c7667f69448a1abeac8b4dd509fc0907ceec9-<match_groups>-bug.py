def match_groups(self, server_info, tags):
    server_zone = server_info['location']['zone_id']
    server_tags = server_info['tags']
    if (tags is None):
        return set(server_tags).union((server_zone,))
    matching_tags = set(server_tags).intersection(tags)
    if (not matching_tags):
        return set()
    else:
        return matching_tags.union((server_zone,))