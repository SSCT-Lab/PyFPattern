def main():
    module = AnsibleModule(argument_spec={
        
    }, supports_check_mode=True)
    if (module._name == 'ec2_facts'):
        module.deprecate("The 'ec2_facts' module is being renamed 'ec2_metadata_facts'", version=2.7)
    ec2_metadata_facts = Ec2Metadata(module).run()
    ec2_metadata_facts_result = dict(changed=False, ansible_facts=ec2_metadata_facts)
    module.exit_json(**ec2_metadata_facts_result)