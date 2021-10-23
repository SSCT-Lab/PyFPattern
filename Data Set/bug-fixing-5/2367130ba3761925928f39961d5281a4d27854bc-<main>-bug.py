def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(name=dict(type='str'), uuid=dict(type='str'), datacenter=dict(removed_in_version=2.9, type='str', required=True))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['name', 'uuid']])
    pyv = PyVmomiHelper(module)
    folders = pyv.getvm_folder_paths()
    if folders:
        try:
            module.exit_json(folders=folders)
        except Exception as exc:
            module.fail_json(msg=('Folder enumeration failed with exception %s' % to_native(exc)))
    else:
        module.fail_json(msg=('Unable to find folders for virtual machine %s' % (module.params.get('name') or module.params.get('uuid'))))