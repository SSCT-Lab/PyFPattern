

def main():
    module = AnsibleModule(argument_spec=dict(boot=dict(type='bool', default=True), dump=dict(type='str'), fstab=dict(type='str'), fstype=dict(type='str'), path=dict(type='path', required=True, aliases=['name']), opts=dict(type='str'), passno=dict(type='str'), src=dict(type='path'), backup=dict(type='bool', default=False), state=dict(type='str', required=True, choices=['absent', 'mounted', 'present', 'unmounted', 'remounted'])), supports_check_mode=True, required_if=(['state', 'mounted', ['src', 'fstype']], ['state', 'present', ['src', 'fstype']]))
    if (get_platform().lower() == 'sunos'):
        args = dict(name=module.params['path'], opts='-', passno='-', fstab=module.params['fstab'], boot='yes')
        if (args['fstab'] is None):
            args['fstab'] = '/etc/vfstab'
    else:
        args = dict(name=module.params['path'], opts='defaults', dump='0', passno='0', fstab=module.params['fstab'])
        if (args['fstab'] is None):
            args['fstab'] = '/etc/fstab'
        if (get_platform() == 'FreeBSD'):
            args['opts'] = 'rw'
    linux_mounts = []
    if (get_platform() == 'Linux'):
        linux_mounts = get_linux_mounts(module)
        if (linux_mounts is None):
            args['warnings'] = 'Cannot open file /proc/self/mountinfo. Bind mounts might be misinterpreted.'
    for key in ('src', 'fstype', 'passno', 'opts', 'dump', 'fstab'):
        if (module.params[key] is not None):
            args[key] = module.params[key]
    if (not os.path.exists(args['fstab'])):
        if (not os.path.exists(os.path.dirname(args['fstab']))):
            os.makedirs(os.path.dirname(args['fstab']))
        try:
            open(args['fstab'], 'a').close()
        except PermissionError as e:
            module.fail_json(msg=('Failed to open %s due to permission issue' % args['fstab']))
        except Exception as e:
            module.fail_json(msg=('Failed to open %s due to %s' % (args['fstab'], to_native(e))))
    state = module.params['state']
    name = module.params['path']
    changed = False
    if (state == 'absent'):
        (name, changed) = unset_mount(module, args)
        if (changed and (not module.check_mode)):
            if (ismount(name) or is_bind_mounted(module, linux_mounts, name)):
                (res, msg) = umount(module, name)
                if res:
                    module.fail_json(msg=('Error unmounting %s: %s' % (name, msg)))
            if os.path.exists(name):
                try:
                    os.rmdir(name)
                except (OSError, IOError) as e:
                    module.fail_json(msg=('Error rmdir %s: %s' % (name, to_native(e))))
    elif (state == 'unmounted'):
        if (ismount(name) or is_bind_mounted(module, linux_mounts, name)):
            if (not module.check_mode):
                (res, msg) = umount(module, name)
                if res:
                    module.fail_json(msg=('Error unmounting %s: %s' % (name, msg)))
            changed = True
    elif (state == 'mounted'):
        if (not os.path.exists(args['src'])):
            module.fail_json(msg=('Unable to mount %s as it does not exist' % args['src']))
        if ((not os.path.exists(name)) and (not module.check_mode)):
            try:
                os.makedirs(name)
            except (OSError, IOError) as e:
                module.fail_json(msg=('Error making dir %s: %s' % (name, to_native(e))))
        (name, changed) = set_mount(module, args)
        res = 0
        if (ismount(name) or is_bind_mounted(module, linux_mounts, name, args['src'], args['fstype'])):
            if (changed and (not module.check_mode)):
                (res, msg) = remount(module, args)
                changed = True
        else:
            changed = True
            if (not module.check_mode):
                (res, msg) = mount(module, args)
        if res:
            module.fail_json(msg=('Error mounting %s: %s' % (name, msg)))
    elif (state == 'present'):
        (name, changed) = set_mount(module, args)
    elif (state == 'remounted'):
        if (not module.check_mode):
            (res, msg) = remount(module, args)
            if res:
                module.fail_json(msg=('Error remounting %s: %s' % (name, msg)))
        changed = True
    else:
        module.fail_json(msg='Unexpected position reached')
    module.exit_json(changed=changed, **args)
