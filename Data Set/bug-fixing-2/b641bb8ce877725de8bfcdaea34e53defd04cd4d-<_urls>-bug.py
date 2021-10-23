

def _urls(self, page, protocol, domain):
    urls = []
    last_mods = set()
    for item in self.paginator.page(page).object_list:
        for url_info in item.get_sitemap_urls():
            urls.append(url_info)
            last_mods.add(url_info.get('lastmod'))
    if (None not in last_mods):
        self.latest_lastmod = max(last_mods)
    return urls
