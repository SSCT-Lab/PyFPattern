def json_format_dict(self, data, pretty=False):
    ' Converts a dict to a JSON object and dumps it as a formatted\n        string '
    if pretty:
        return json.dumps(data, sort_keys=True, indent=2)
    else:
        return json.dumps(data)