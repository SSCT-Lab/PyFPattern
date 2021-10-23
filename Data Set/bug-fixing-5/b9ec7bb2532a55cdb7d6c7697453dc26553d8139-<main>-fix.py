def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(name=dict(type='str'), name_match=dict(type='str', choices=['first', 'last'], default='first'), uuid=dict(type='str'), use_instance_uuid=dict(type='bool', default=False), dest_folder=dict(type='str', required=True), datacenter=dict(type='str', required=True))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['name', 'uuid']])
    module.params['dest_folder'] = module.params['dest_folder'].rstrip('/')
    pyv = PyVmomiHelper(module)
    search_index = pyv.content.searchIndex
    vm = pyv.get_vm()
    if vm:
        try:
            vm_path = pyv.get_vm_path(pyv.content, vm).lstrip('/')
            vm_full = ((vm_path + '/') + module.params['name'])
            folder = search_index.FindByInventoryPath(module.params['dest_folder'])
            if (folder is None):
                module.fail_json(msg='Folder name and/or path does not exist')
            vm_to_move = search_index.FindByInventoryPath(vm_full)
            if (vm_path != module.params['dest_folder'].lstrip('/')):
                move_task = folder.MoveInto([vm_to_move])
                (changed, err) = wait_for_task(move_task)
                if changed:
                    module.exit_json(changed=True, instance=pyv.gather_facts(vm))
            else:
                module.exit_json(instance=pyv.gather_facts(vm))
        except Exception as exc:
            module.fail_json(msg=('Failed to move VM with exception %s' % to_native(exc)))
    else:
        module.fail_json(msg=('Unable to find VM %s to move to %s' % ((module.params.get('uuid') or module.params.get('name')), module.params.get('dest_folder'))))