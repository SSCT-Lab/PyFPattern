def build_absolute_uri(self, location=None):
    '\n        Build an absolute URI from the location and the variables available in\n        this request. If no ``location`` is specified, bulid the absolute URI\n        using request.get_full_path(). If the location is absolute, convert it\n        to an RFC 3987 compliant URI and return it. If location is relative or\n        is scheme-relative (i.e., ``//example.com/``), urljoin() it to a base\n        URL constructed from the request variables.\n        '
    if (location is None):
        location = ('//%s' % self.get_full_path())
    bits = urlsplit(location)
    if (not (bits.scheme and bits.netloc)):
        if (bits.path.startswith('/') and (not bits.scheme) and (not bits.netloc) and ('/./' not in bits.path) and ('/../' not in bits.path)):
            if location.startswith('//'):
                location = location[2:]
            location = (self._current_scheme_host + location)
        else:
            location = urljoin((self._current_scheme_host + self.path), location)
    return iri_to_uri(location)