@staticmethod
def _parse_links(links):
    '\n        Turn links into a dictionary\n        '
    if (links is None):
        return None
    result = {
        
    }
    for link in links:
        parsed_link = link.split(':', 1)
        if (len(parsed_link) == 2):
            result[parsed_link[0]] = parsed_link[1]
        else:
            result[parsed_link[0]] = parsed_link[0]
    return result