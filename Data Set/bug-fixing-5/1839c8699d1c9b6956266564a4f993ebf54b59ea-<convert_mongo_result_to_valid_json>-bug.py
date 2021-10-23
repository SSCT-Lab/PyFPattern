def convert_mongo_result_to_valid_json(self, result):
    if (result is None):
        return result
    if isinstance(result, (int, long, float, bool)):
        return result
    if isinstance(result, string_types):
        return result
    elif isinstance(result, list):
        new_list = []
        for elem in result:
            new_list.append(self.convert_mongo_result_to_valid_json(elem))
        return new_list
    elif isinstance(result, dict):
        new_dict = {
            
        }
        for key in result.keys():
            value = reslut[key]
            new_dict[key] = self.convert_mongo_result_to_valid_json(value)
        return new_dict
    elif isinstance(result, datetime.datetime):
        return (result - datetime.datetime(1970, 1, 1)).total_seconds()
    else:
        return '{}'.format(result)