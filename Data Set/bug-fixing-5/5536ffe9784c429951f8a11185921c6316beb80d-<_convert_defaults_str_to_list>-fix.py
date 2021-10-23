@staticmethod
def _convert_defaults_str_to_list(value):
    value = value.splitlines()
    value.pop(0)
    value.pop((- 1))
    value = [re.sub(',$', '', x.strip(' ')) for x in value]
    return value