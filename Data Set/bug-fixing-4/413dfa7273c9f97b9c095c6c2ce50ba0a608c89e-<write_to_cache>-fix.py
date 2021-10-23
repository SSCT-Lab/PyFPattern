def write_to_cache(self, data, filename):
    ' Writes data in JSON format to a file '
    json_data = self.json_format_dict(data, True)
    with open(filename, 'w') as f:
        f.write(json_data)