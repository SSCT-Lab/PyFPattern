def delete(self, name):

    def _try_delete():
        normalized_name = self._normalize_name(clean_name(name))
        self.bucket.delete_blob(self._encode_name(normalized_name))
    try:
        try_repeated(_try_delete)
    except NotFound:
        pass