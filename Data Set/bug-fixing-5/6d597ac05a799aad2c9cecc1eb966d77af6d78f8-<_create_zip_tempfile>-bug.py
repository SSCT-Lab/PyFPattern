def _create_zip_tempfile(self, files, directories):
    tmpdir = tempfile.mkdtemp()
    zip_file_path = os.path.join(tmpdir, 'win_copy.zip')
    zip_file = zipfile.ZipFile(zip_file_path, 'w')
    for directory in directories:
        directory_path = to_bytes(directory['src'], errors='surrogate_or_strict')
        archive_path = to_bytes(directory['dest'], errors='surrogate_or_strict')
        encoded_path = to_text(base64.b64encode(archive_path), errors='surrogate_or_strict')
        zip_file.write(directory_path, encoded_path, zipfile.ZIP_DEFLATED)
    for file in files:
        file_path = to_bytes(file['src'], errors='surrogate_or_strict')
        archive_path = to_bytes(file['dest'], errors='surrogate_or_strict')
        encoded_path = to_text(base64.b64encode(archive_path), errors='surrogate_or_strict')
        zip_file.write(file_path, encoded_path, zipfile.ZIP_DEFLATED)
    return zip_file_path