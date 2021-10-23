def download(self, tmpdir, artifact, verify_download, filename=None):
    if ((not artifact.version) or (artifact.version == 'latest')):
        artifact = Artifact(artifact.group_id, artifact.artifact_id, self.find_latest_version_available(artifact), artifact.classifier, artifact.extension)
    url = self.find_uri_for_artifact(artifact)
    (tempfd, tempname) = tempfile.mkstemp(dir=tmpdir)
    try:
        if self.local:
            parsed_url = urlparse(url)
            if os.path.isfile(parsed_url.path):
                shutil.copy2(parsed_url.path, tempname)
            else:
                return ('Can not find local file: ' + parsed_url.path)
        else:
            response = self._request(url, ('Failed to download artifact ' + str(artifact)))
            with os.fdopen(tempfd, 'wb') as f:
                shutil.copyfileobj(response, f)
        if verify_download:
            invalid_md5 = self.is_invalid_md5(tempname, url)
            if invalid_md5:
                os.remove(tempname)
                return invalid_md5
    except Exception as e:
        os.remove(tempname)
        raise e
    shutil.move(tempname, artifact.get_filename(filename))
    return None