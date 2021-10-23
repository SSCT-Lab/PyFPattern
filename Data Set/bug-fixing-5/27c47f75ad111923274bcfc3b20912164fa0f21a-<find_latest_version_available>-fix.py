def find_latest_version_available(self, artifact):
    if self.latest_version_found:
        return self.latest_version_found
    path = ('/%s/%s' % (artifact.path(False), self.metadata_file_name))
    content = self._getContent((self.base + path), ('Failed to retrieve the maven metadata file: ' + path))
    xml = etree.fromstring(content)
    v = xml.xpath('/metadata/versioning/versions/version[last()]/text()')
    if v:
        self.latest_version_found = v[0]
        return v[0]