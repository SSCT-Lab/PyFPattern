def find_uri_for_artifact(self, artifact):
    if (artifact.version == 'latest'):
        artifact.version = self.find_latest_version_available(artifact)
    if artifact.is_snapshot():
        if self.local:
            return self._uri_for_artifact(artifact, artifact.version)
        path = ('/%s/%s' % (artifact.path(), self.metadata_file_name))
        content = self._getContent((self.base + path), ('Failed to retrieve the maven metadata file: ' + path))
        xml = etree.fromstring(content)
        for snapshotArtifact in xml.xpath('/metadata/versioning/snapshotVersions/snapshotVersion'):
            classifier = snapshotArtifact.xpath('classifier/text()')
            artifact_classifier = (classifier[0] if classifier else '')
            extension = snapshotArtifact.xpath('extension/text()')
            artifact_extension = (extension[0] if extension else '')
            if ((artifact_classifier == artifact.classifier) and (artifact_extension == artifact.extension)):
                return self._uri_for_artifact(artifact, snapshotArtifact.xpath('value/text()')[0])
        timestamp_xmlpath = xml.xpath('/metadata/versioning/snapshot/timestamp/text()')
        if timestamp_xmlpath:
            timestamp = timestamp_xmlpath[0]
            build_number = xml.xpath('/metadata/versioning/snapshot/buildNumber/text()')[0]
            return self._uri_for_artifact(artifact, artifact.version.replace('SNAPSHOT', ((timestamp + '-') + build_number)))
    return self._uri_for_artifact(artifact, artifact.version)