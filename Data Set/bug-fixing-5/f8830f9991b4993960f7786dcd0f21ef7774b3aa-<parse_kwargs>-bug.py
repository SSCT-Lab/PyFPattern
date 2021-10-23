def parse_kwargs(desc):
    "Maps a description of args to a dictionary of {argname: description}.\n    Input:\n        ('    weight (Tensor): a weight tensor\n' +\n         '        Some optional description')\n    Output: {\n        'weight':         'weight (Tensor): a weight tensor\n        Some optional description'\n    }\n    "
    kwargs = [section.strip() for section in desc.split('\n   ')]
    kwargs = [section for section in kwargs if (len(section) > 0)]
    return {desc.split(' ')[0]: desc for desc in kwargs}