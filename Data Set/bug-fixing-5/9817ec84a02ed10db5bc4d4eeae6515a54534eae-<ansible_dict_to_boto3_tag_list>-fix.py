def ansible_dict_to_boto3_tag_list(tags_dict, tag_name_key_name='Key', tag_value_key_name='Value'):
    ' Convert a flat dict of key:value pairs representing AWS resource tags to a boto3 list of dicts\n    Args:\n        tags_dict (dict): Dict representing AWS resource tags.\n        tag_name_key_name (str): Value to use as the key for all tag keys (useful because boto3 doesn\'t always use "Key")\n        tag_value_key_name (str): Value to use as the key for all tag values (useful because boto3 doesn\'t always use "Value")\n    Basic Usage:\n        >>> tags_dict = {\'MyTagKey\': \'MyTagValue\'}\n        >>> ansible_dict_to_boto3_tag_list(tags_dict)\n        {\n            \'MyTagKey\': \'MyTagValue\'\n        }\n    Returns:\n        List: List of dicts containing tag keys and values\n        [\n            {\n                \'Key\': \'MyTagKey\',\n                \'Value\': \'MyTagValue\'\n            }\n        ]\n    '
    tags_list = []
    for (k, v) in tags_dict.items():
        tags_list.append({
            tag_name_key_name: k,
            tag_value_key_name: to_native(v),
        })
    return tags_list