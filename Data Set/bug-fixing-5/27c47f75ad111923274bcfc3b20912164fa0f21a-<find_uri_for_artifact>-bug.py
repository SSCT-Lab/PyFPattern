def find_uri_for_artifact(self, artifact):
    if (artifact.version == 'latest'):
        artifact.version = self.find_latest_version_available(artifact)
    if artifact.is_snapshot():
        path = ('/%s/maven-metadata.xml' % artifact.path())
        xml = self._request((self.base + path), 'Failed to download maven-metadata.xml', etree.parse)
        timestamp = xml.xpath('/metadata/versioning/snapshot/timestamp/text()')[0]
        buildNumber = xml.xpath('/metadata/versioning/snapshot/buildNumber/text()')[0]
        for snapshotArtifact in xml.xpath('/metadata/versioning/snapshotVersions/snapshotVersion'):
            classifier = snapshotArtifact.xpath('classifier/text()')
            artifact_classifier = (classifier[0] if classifier else '')
            extension = snapshotArtifact.xpath('extension/text()')
            artifact_extension = (extension[0] if extension else '')
            if ((artifact_classifier == artifact.classifier) and (artifact_extension == artifact.extension)):
                return self._uri_for_artifact(artifact, snapshotArtifact.xpath('value/text()')[0])
        return self._uri_for_artifact(artifact, artifact.version.replace('SNAPSHOT', ((timestamp + '-') + buildNumber)))
    return self._uri_for_artifact(artifact, artifact.version)