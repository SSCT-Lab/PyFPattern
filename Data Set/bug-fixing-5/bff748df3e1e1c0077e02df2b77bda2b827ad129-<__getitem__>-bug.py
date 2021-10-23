def __getitem__(self, key):
    key = key.lower()
    try:
        return self.base_data_types_reverse[key]
    except KeyError:
        size = get_field_size(key)
        if (size is not None):
            return ('CharField', {
                'max_length': size,
            })
        raise KeyError