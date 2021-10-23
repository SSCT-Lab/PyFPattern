def _real_extract(self, url):
    (webpage, info) = self._extract_info(url)
    info['view_count'] = str_to_int(self._search_regex('<b>([\\d,.]+)</b> Views?', webpage, 'view count', fatal=False))
    return info