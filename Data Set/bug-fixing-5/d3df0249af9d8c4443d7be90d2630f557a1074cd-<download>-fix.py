def download(self, artifact, verify_download, filename=None):
    filename = artifact.get_filename(filename)
    if ((not artifact.version) or (artifact.version == 'latest')):
        artifact = Artifact(artifact.group_id, artifact.artifact_id, self.find_latest_version_available(artifact), artifact.classifier, artifact.extension)
    url = self.find_uri_for_artifact(artifact)
    error = None
    response = self._request(url, ('Failed to download artifact ' + str(artifact)), (lambda r: r))
    if response:
        f = open(filename, 'wb')
        self._write_chunks(response, f, report_hook=self.chunk_report)
        f.close()
        with open(filename, 'wb') as f:
            self._write_chunks(response, f, report_hook=self.chunk_report)
        if (verify_download and (not self.verify_md5(filename, (url + '.md5')))):
            os.remove(filename)
            error = 'Checksum verification failed'
        else:
            error = None
    else:
        error = ('Error downloading artifact ' + str(artifact))
    return error