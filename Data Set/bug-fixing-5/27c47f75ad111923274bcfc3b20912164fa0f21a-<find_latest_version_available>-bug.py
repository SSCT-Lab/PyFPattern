def find_latest_version_available(self, artifact):
    if self.latest_version_found:
        return self.latest_version_found
    path = ('/%s/maven-metadata.xml' % artifact.path(False))
    xml = self._request((self.base + path), 'Failed to download maven-metadata.xml', etree.parse)
    v = xml.xpath('/metadata/versioning/versions/version[last()]/text()')
    if v:
        self.latest_version_found = v[0]
        return v[0]