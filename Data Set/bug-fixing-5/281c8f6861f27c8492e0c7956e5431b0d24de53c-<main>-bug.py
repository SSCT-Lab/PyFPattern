def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(datacenter=dict(type='str', required=False), cluster_name=dict(type='str', required=False))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['cluster_name', 'datacenter']])
    vmware_drs_facts = VmwareDrsFactManager(module)
    module.exit_json(changed=False, drs_rule_facts=vmware_drs_facts.gather_drs_rule_facts())