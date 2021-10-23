def _get_boto_attr_chain(self, filter_name, instance):
    '\n            :param filter_name: The filter\n            :param instance: A namedtuple\n        '
    allowed_filters = sorted((list(instance_data_filter_to_boto_attr.keys()) + list(instance_meta_filter_to_boto_attr.keys())))
    if (filter_name not in allowed_filters):
        raise AnsibleError(("Invalid filter '%s' provided; filter must be one of %s." % (filter_name, allowed_filters)))
    if (filter_name in instance_data_filter_to_boto_attr):
        boto_attr_list = instance_data_filter_to_boto_attr[filter_name]
    else:
        boto_attr_list = instance_meta_filter_to_boto_attr[filter_name]
    instance_value = instance
    for attribute in boto_attr_list:
        instance_value = self._compile_values(instance_value, attribute)
    return instance_value