def main():
    state_map = dict(present='install', absent='uninstall -y', latest='install -U', forcereinstall='install -U --force-reinstall')
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=state_map.keys()), name=dict(type='list'), version=dict(type='str'), requirements=dict(), virtualenv=dict(type='path'), virtualenv_site_packages=dict(default=False, type='bool'), virtualenv_command=dict(default='virtualenv', type='path'), virtualenv_python=dict(type='str'), use_mirrors=dict(default=True, type='bool'), extra_args=dict(), editable=dict(default=True, type='bool'), chdir=dict(type='path'), executable=dict(type='path'), umask=dict()), required_one_of=[['name', 'requirements']], mutually_exclusive=[['name', 'requirements'], ['executable', 'virtualenv']], supports_check_mode=True)
    state = module.params['state']
    name = module.params['name']
    version = module.params['version']
    requirements = module.params['requirements']
    extra_args = module.params['extra_args']
    virtualenv_python = module.params['virtualenv_python']
    chdir = module.params['chdir']
    umask = module.params['umask']
    if (umask and (not isinstance(umask, int))):
        try:
            umask = int(umask, 8)
        except Exception:
            module.fail_json(msg='umask must be an octal integer', details=to_native(sys.exc_info()[1]))
    old_umask = None
    if (umask is not None):
        old_umask = os.umask(umask)
    try:
        if ((state == 'latest') and (version is not None)):
            module.fail_json(msg='version is incompatible with state=latest')
        if (chdir is None):
            chdir = tempfile.gettempdir()
        err = ''
        out = ''
        env = module.params['virtualenv']
        if env:
            if (not os.path.exists(os.path.join(env, 'bin', 'activate'))):
                if module.check_mode:
                    module.exit_json(changed=True)
                cmd = module.params['virtualenv_command']
                if (os.path.basename(cmd) == cmd):
                    cmd = module.get_bin_path(cmd, True)
                if module.params['virtualenv_site_packages']:
                    cmd += ' --system-site-packages'
                else:
                    cmd_opts = _get_cmd_options(module, cmd)
                    if ('--no-site-packages' in cmd_opts):
                        cmd += ' --no-site-packages'
                if virtualenv_python:
                    cmd += (' -p%s' % virtualenv_python)
                elif PY3:
                    cmd += (' -p%s' % sys.executable)
                cmd = ('%s %s' % (cmd, env))
                (rc, out_venv, err_venv) = module.run_command(cmd, cwd=chdir)
                out += out_venv
                err += err_venv
                if (rc != 0):
                    _fail(module, cmd, out, err)
        pip = _get_pip(module, env, module.params['executable'])
        cmd = ('%s %s' % (pip, state_map[state]))
        path_prefix = None
        if env:
            path_prefix = '/'.join(pip.split('/')[:(- 1)])
        has_vcs = False
        if name:
            for pkg in name:
                if bool((pkg and re.match('(svn|git|hg|bzr)\\+', pkg))):
                    has_vcs = True
                    break
        if (has_vcs and module.params['editable']):
            args_list = []
            if extra_args:
                args_list = extra_args.split(' ')
            if ('-e' not in args_list):
                args_list.append('-e')
                extra_args = ' '.join(args_list)
        if extra_args:
            cmd += (' %s' % extra_args)
        if name:
            for pkg in name:
                cmd += (' %s' % _get_full_name(pkg, version))
        elif requirements:
            cmd += (' -r %s' % requirements)
        if module.check_mode:
            if (extra_args or requirements or (state == 'latest') or (not name)):
                module.exit_json(changed=True)
            elif has_vcs:
                module.exit_json(changed=True)
            (pkg_cmd, out_pip, err_pip) = _get_packages(module, pip, chdir)
            out += out_pip
            err += err_pip
            changed = False
            if name:
                pkg_list = [p for p in out.split('\n') if ((not p.startswith('You are using')) and (not p.startswith('You should consider')) and p)]
                if (pkg_cmd.endswith(' freeze') and (('pip' in name) or ('setuptools' in name))):
                    for pkg in ('setuptools', 'pip'):
                        if (pkg in name):
                            formatted_dep = _get_package_info(module, pkg, env)
                            if (formatted_dep is not None):
                                pkg_list.append(formatted_dep)
                                out += ('%s\n' % formatted_dep)
                for pkg in name:
                    is_present = _is_present(pkg, version, pkg_list, pkg_cmd)
                    if (((state == 'present') and (not is_present)) or ((state == 'absent') and is_present)):
                        changed = True
                        break
            module.exit_json(changed=changed, cmd=pkg_cmd, stdout=out, stderr=err)
        if (requirements or has_vcs):
            (_, out_freeze_before, _) = _get_packages(module, pip, chdir)
        else:
            out_freeze_before = None
        (rc, out_pip, err_pip) = module.run_command(cmd, path_prefix=path_prefix, cwd=chdir)
        out += out_pip
        err += err_pip
        if ((rc == 1) and (state == 'absent') and (('not installed' in out_pip) or ('not installed' in err_pip))):
            pass
        elif (rc != 0):
            _fail(module, cmd, out, err)
        if (state == 'absent'):
            changed = ('Successfully uninstalled' in out_pip)
        elif (out_freeze_before is None):
            changed = ('Successfully installed' in out_pip)
        elif (out_freeze_before is None):
            changed = ('Successfully installed' in out_pip)
        else:
            (_, out_freeze_after, _) = _get_packages(module, pip, chdir)
            changed = (out_freeze_before != out_freeze_after)
        module.exit_json(changed=changed, cmd=cmd, name=name, version=version, state=state, requirements=requirements, virtualenv=env, stdout=out, stderr=err)
    finally:
        if (old_umask is not None):
            os.umask(old_umask)