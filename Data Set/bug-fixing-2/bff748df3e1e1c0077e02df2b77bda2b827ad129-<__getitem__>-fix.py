

def __getitem__(self, key):
    key = key.lower().split('(', 1)[0].strip()
    return self.base_data_types_reverse[key]
