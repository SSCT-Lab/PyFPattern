def _get_hostname(self, instance, hostnames):
    '\n            :param instance: an instance dict returned by boto3 ec2 describe_instances()\n            :param hostnames: a list of hostname destination variables in order of preference\n            :return the preferred identifer for the host\n        '
    if (not hostnames):
        hostnames = ['dns-name', 'private-dns-name']
    hostname = None
    for preference in hostnames:
        if ('tag' in preference):
            if (not preference.startswith('tag:')):
                raise AnsibleError("To name a host by tags name_value, use 'tag:name=value'.")
            hostname = self._get_tag_hostname(preference, instance)
        else:
            hostname = self._get_boto_attr_chain(preference, instance)
        if hostname:
            break
    if hostname:
        if (':' in to_text(hostname)):
            return to_safe_group_name(to_text(hostname))
        else:
            return to_text(hostname)