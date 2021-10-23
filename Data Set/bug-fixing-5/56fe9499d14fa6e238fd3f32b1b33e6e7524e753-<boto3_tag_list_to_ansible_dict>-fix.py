def boto3_tag_list_to_ansible_dict(tags_list, tag_name_key_name=None, tag_value_key_name=None):
    ' Convert a boto3 list of resource tags to a flat dict of key:value pairs\n    Args:\n        tags_list (list): List of dicts representing AWS tags.\n        tag_name_key_name (str): Value to use as the key for all tag keys (useful because boto3 doesn\'t always use "Key")\n        tag_value_key_name (str): Value to use as the key for all tag values (useful because boto3 doesn\'t always use "Value")\n    Basic Usage:\n        >>> tags_list = [{\'Key\': \'MyTagKey\', \'Value\': \'MyTagValue\'}]\n        >>> boto3_tag_list_to_ansible_dict(tags_list)\n        [\n            {\n                \'Key\': \'MyTagKey\',\n                \'Value\': \'MyTagValue\'\n            }\n        ]\n    Returns:\n        Dict: Dict of key:value pairs representing AWS tags\n         {\n            \'MyTagKey\': \'MyTagValue\',\n        }\n    '
    if (tag_name_key_name and tag_value_key_name):
        tag_candidates = {
            tag_name_key_name: tag_value_key_name,
        }
    else:
        tag_candidates = {
            'key': 'value',
            'Key': 'Value',
        }
    if (not tags_list):
        return {
            
        }
    for (k, v) in tag_candidates.items():
        if ((k in tags_list[0]) and (v in tags_list[0])):
            return dict(((tag[k], tag[v]) for tag in tags_list))
    raise ValueError(("Couldn't find tag key (candidates %s) in tag list %s" % (str(tag_candidates), str(tags_list))))