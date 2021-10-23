def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(portgroup_name=dict(required=True, type='str'), switch_name=dict(required=True, type='str'), vlan_id=dict(required=True, type='int'), hosts=dict(type='list', aliases=['esxi_hostname']), cluster_name=dict(type='str'), state=dict(type='str', choices=['present', 'absent'], default='present'), network_policy=dict(type='dict', options=dict(promiscuous_mode=dict(type='bool'), forged_transmits=dict(type='bool'), mac_changes=dict(type='bool')), default=dict(promiscuous_mode=False, forged_transmits=False, mac_changes=False))))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False, required_one_of=[['cluster_name', 'hosts']])
    try:
        pyv = PyVmomiHelper(module)
        pyv.process_state()
    except vmodl.RuntimeFault as runtime_fault:
        module.fail_json(msg=to_native(runtime_fault.msg))
    except vmodl.MethodFault as method_fault:
        module.fail_json(msg=to_native(method_fault.msg))
    except Exception as e:
        module.fail_json(msg=to_native(e))