def delete(self, name):
    name = self._normalize_name(clean_name(name))
    try:
        self.bucket.delete_blob(self._encode_name(name))
    except NotFound:
        pass