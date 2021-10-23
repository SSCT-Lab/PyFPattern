def boto3_tag_list_to_ansible_dict(tags_list, tag_name_key_name='Key', tag_value_key_name='Value'):
    ' Convert a boto3 list of resource tags to a flat dict of key:value pairs\n    Args:\n        tags_list (list): List of dicts representing AWS tags.\n        tag_name_key_name (str): Value to use as the key for all tag keys (useful because boto3 doesn\'t always use "Key")\n        tag_value_key_name (str): Value to use as the key for all tag values (useful because boto3 doesn\'t always use "Value")\n    Basic Usage:\n        >>> tags_list = [{\'Key\': \'MyTagKey\', \'Value\': \'MyTagValue\'}]\n        >>> boto3_tag_list_to_ansible_dict(tags_list)\n        [\n            {\n                \'Key\': \'MyTagKey\',\n                \'Value\': \'MyTagValue\'\n            }\n        ]\n    Returns:\n        Dict: Dict of key:value pairs representing AWS tags\n         {\n            \'MyTagKey\': \'MyTagValue\',\n        }\n    '
    tags_dict = {
        
    }
    for tag in tags_list:
        if (tag_name_key_name in tag):
            tags_dict[tag[tag_name_key_name]] = tag[tag_value_key_name]
    return tags_dict