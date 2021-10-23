def _save(self, name, content):
    cleaned_name = clean_name(name)
    name = self._normalize_name(cleaned_name)
    content.name = cleaned_name
    encoded_name = self._encode_name(name)
    file = GoogleCloudFile(encoded_name, 'w', self)
    file.blob.upload_from_file(content, size=content.size, content_type=file.mime_type)
    return cleaned_name