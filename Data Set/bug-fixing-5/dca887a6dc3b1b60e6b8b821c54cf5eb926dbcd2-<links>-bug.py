def links(self):
    links = {
        
    }
    if ('link' in self.info):
        link_header = re.info['link']
        matches = re.findall('<([^>]+)>; rel="([^"]+)"', link_header)
        for (url, rel) in matches:
            links[rel] = url
    return links