def download(self, artifact, verify_download, filename=None):
    filename = artifact.get_filename(filename)
    if ((not artifact.version) or (artifact.version == 'latest')):
        artifact = Artifact(artifact.group_id, artifact.artifact_id, self.find_latest_version_available(artifact), artifact.classifier, artifact.extension)
    url = self.find_uri_for_artifact(artifact)
    if self.local:
        parsed_url = urlparse(url)
        if os.path.isfile(parsed_url.path):
            shutil.copy2(parsed_url.path, filename)
        else:
            return ('Can not find local file: ' + parsed_url.path)
    else:
        response = self._request(url, ('Failed to download artifact ' + str(artifact)))
        with io.open(filename, 'wb') as f:
            self._write_chunks(response, f, report_hook=self.chunk_report)
    if verify_download:
        invalid_md5 = self.is_invalid_md5(filename, url)
        if invalid_md5:
            os.remove(filename)
            return invalid_md5
    return None