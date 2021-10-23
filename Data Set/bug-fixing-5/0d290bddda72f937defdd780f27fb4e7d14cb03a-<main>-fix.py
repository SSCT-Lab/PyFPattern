def main():
    global module
    module = AnsibleModule(argument_spec=dict(filter=dict(default=None, choices=['cloudstack_service_offering', 'cloudstack_availability_zone', 'cloudstack_public_hostname', 'cloudstack_public_ipv4', 'cloudstack_local_hostname', 'cloudstack_local_ipv4', 'cloudstack_instance_id', 'cloudstack_user_data'])), supports_check_mode=False)
    if (not HAS_LIB_YAML):
        module.fail_json(msg='missing python library: yaml')
    cs_facts = CloudStackFacts().run()
    cs_facts_result = dict(changed=False, ansible_facts=cs_facts)
    module.exit_json(**cs_facts_result)