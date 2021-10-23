def main():
    argument_spec = vmware_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_PYVMOMI):
        module.fail_json(msg='pyvmomi is required for this module')
    try:
        content = connect_to_api(module)
        _virtual_machines = get_all_virtual_machines(content)
        module.exit_json(changed=False, virtual_machines=_virtual_machines)
    except vmodl.RuntimeFault as runtime_fault:
        module.fail_json(msg=runtime_fault.msg)
    except vmodl.MethodFault as method_fault:
        module.fail_json(msg=method_fault.msg)
    except Exception as e:
        module.fail_json(msg=str(e))