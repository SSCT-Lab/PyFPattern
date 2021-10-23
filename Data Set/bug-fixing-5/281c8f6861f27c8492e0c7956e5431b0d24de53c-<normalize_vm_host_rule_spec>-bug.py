@staticmethod
def normalize_vm_host_rule_spec(rule_obj=None):
    '\n        Function to return human readable rule spec\n        Args:\n            rule_obj: Rule managed object\n\n        Returns: Dictionary with DRS VM HOST Rule info\n\n        '
    if (rule_obj is None):
        return {
            
        }
    return dict(rule_key=rule_obj.key, rule_enabled=rule_obj.enabled, rule_name=rule_obj.name, rule_mandatory=rule_obj.mandatory, rule_uuid=rule_obj.ruleUuid, rule_vm_group_name=rule_obj.vmGroupName, rule_affine_host_group_name=rule_obj.affineHostGroupName, rule_anti_affine_host_group_name=rule_obj.antiAffineHostGroupName, rule_type='vm_host_rule')