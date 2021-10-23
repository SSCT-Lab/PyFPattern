def check_all_properties(self, host_id, host_groups, status, interfaces, template_ids, exist_interfaces, host, proxy_id, visible_name, description, host_name):
    exist_host_groups = self.get_host_groups_by_host_id(host_id)
    if (set(host_groups) != set(exist_host_groups)):
        return True
    exist_status = self.get_host_status_by_host(host)
    if (int(status) != int(exist_status)):
        return True
    if self.check_interface_properties(exist_interfaces, interfaces):
        return True
    exist_template_ids = self.get_host_templates_by_host_id(host_id)
    if (set(list(template_ids)) != set(exist_template_ids)):
        return True
    if (int(host['proxy_hostid']) != int(proxy_id)):
        return True
    if ((host['name'] != visible_name) and (host['name'] != host_name)):
        return True
    if (description is None):
        description = ''
    if (host['description'] != description):
        return True
    return False