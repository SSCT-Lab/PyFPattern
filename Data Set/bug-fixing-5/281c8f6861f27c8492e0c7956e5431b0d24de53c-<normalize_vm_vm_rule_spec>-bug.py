@staticmethod
def normalize_vm_vm_rule_spec(rule_obj=None):
    '\n        Function to return human readable rule spec\n        Args:\n            rule_obj: Rule managed object\n\n        Returns: Dictionary with DRS VM VM Rule info\n\n        '
    if (rule_obj is None):
        return {
            
        }
    return dict(rule_key=rule_obj.key, rule_enabled=rule_obj.enabled, rule_name=rule_obj.name, rule_mandatory=rule_obj.mandatory, rule_uuid=rule_obj.ruleUuid, rule_vms=[vm.name for vm in rule_obj.vm], rule_type='vm_vm_rule')