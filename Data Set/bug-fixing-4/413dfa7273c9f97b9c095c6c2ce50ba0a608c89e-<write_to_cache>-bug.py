def write_to_cache(self, data, filename):
    ' Writes data in JSON format to a file '
    json_data = self.json_format_dict(data, True)
    cache = open(filename, 'w')
    cache.write(json_data)
    cache.close()