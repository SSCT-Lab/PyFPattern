

def main():
    arg_spec = dict(name=dict(default=None), offline=dict(default='no', type='bool'), production=dict(default='no', type='bool'), path=dict(required=True, type='path'), relative_execpath=dict(default=None, required=False, type='path'), state=dict(default='present', choices=['present', 'absent', 'latest']), version=dict(default=None))
    module = AnsibleModule(argument_spec=arg_spec)
    name = module.params['name']
    offline = module.params['offline']
    production = module.params['production']
    path = os.path.expanduser(module.params['path'])
    relative_execpath = module.params['relative_execpath']
    state = module.params['state']
    version = module.params['version']
    if ((state == 'absent') and (not name)):
        module.fail_json(msg='uninstalling a package is only available for named packages')
    bower = Bower(module, name=name, offline=offline, production=production, path=path, relative_execpath=relative_execpath, version=version)
    changed = False
    if (state == 'present'):
        (installed, missing, outdated) = bower.list()
        if len(missing):
            changed = True
            bower.install()
    elif (state == 'latest'):
        (installed, missing, outdated) = bower.list()
        if (len(missing) or len(outdated)):
            changed = True
            bower.update()
    else:
        (installed, missing, outdated) = bower.list()
        if (name in installed):
            changed = True
            bower.uninstall()
    module.exit_json(changed=changed)
