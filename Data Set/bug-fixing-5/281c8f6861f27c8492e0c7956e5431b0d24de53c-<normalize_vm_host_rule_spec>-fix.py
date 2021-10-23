def normalize_vm_host_rule_spec(self, rule_obj=None, cluster_obj=None):
    '\n        Return human readable rule spec\n        Args:\n            rule_obj: Rule managed object\n            cluster_obj: Cluster managed object\n\n        Returns: Dictionary with DRS VM HOST Rule info\n\n        '
    if (not all([rule_obj, cluster_obj])):
        return {
            
        }
    return dict(rule_key=rule_obj.key, rule_enabled=rule_obj.enabled, rule_name=rule_obj.name, rule_mandatory=rule_obj.mandatory, rule_uuid=rule_obj.ruleUuid, rule_vm_group_name=rule_obj.vmGroupName, rule_affine_host_group_name=rule_obj.affineHostGroupName, rule_anti_affine_host_group_name=rule_obj.antiAffineHostGroupName, rule_vms=self.get_all_from_group(group_name=rule_obj.vmGroupName, cluster_obj=cluster_obj), rule_affine_hosts=self.get_all_from_group(group_name=rule_obj.affineHostGroupName, cluster_obj=cluster_obj, hostgroup=True), rule_anti_affine_hosts=self.get_all_from_group(group_name=rule_obj.antiAffineHostGroupName, cluster_obj=cluster_obj, hostgroup=True), rule_type='vm_host_rule')