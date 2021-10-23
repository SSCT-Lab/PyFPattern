def get_cached_photo(self, size):
    if (not self.file):
        return
    if (size not in self.ALLOWED_SIZES):
        size = min(self.ALLOWED_SIZES, key=(lambda x: abs((x - size))))
    cache_key = self.get_cache_key(size)
    photo = cache.get(cache_key)
    if (photo is None):
        photo_file = self.file.getfile()
        with Image.open(photo_file) as image:
            image = image.resize((size, size))
            image_file = BytesIO()
            image.save(image_file, 'PNG')
            photo = image_file.getvalue()
            cache.set(cache_key, photo)
    return photo