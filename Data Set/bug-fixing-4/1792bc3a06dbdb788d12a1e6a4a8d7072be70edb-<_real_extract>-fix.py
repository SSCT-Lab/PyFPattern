def _real_extract(self, url):
    (webpage, info) = self._extract_info(url, fatal=False)
    if (not info['formats']):
        return self.url_result(url, 'Generic')
    info['view_count'] = str_to_int(self._search_regex('<b>([\\d,.]+)</b> Views?', webpage, 'view count', fatal=False))
    return info