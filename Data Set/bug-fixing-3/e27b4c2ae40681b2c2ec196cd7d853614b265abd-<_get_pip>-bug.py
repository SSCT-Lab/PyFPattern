def _get_pip(module, env=None, executable=None):
    candidate_pip_basenames = ('pip2', 'pip')
    if PY3:
        candidate_pip_basenames = ('pip3',)
    pip = None
    if (executable is not None):
        executable = os.path.expanduser(executable)
        if os.path.isabs(executable):
            pip = executable
        else:
            candidate_pip_basenames = (executable,)
    if (pip is None):
        if (env is None):
            opt_dirs = []
            for basename in candidate_pip_basenames:
                pip = module.get_bin_path(basename, False, opt_dirs)
                if (pip is not None):
                    break
            else:
                module.fail_json(msg=('Unable to find any of %s to use.  pip needs to be installed.' % ', '.join(candidate_pip_basenames)))
        else:
            venv_dir = os.path.join(env, 'bin')
            candidate_pip_basenames = (candidate_pip_basenames[0], 'pip')
            for basename in candidate_pip_basenames:
                candidate = os.path.join(venv_dir, basename)
                if (os.path.exists(candidate) and is_executable(candidate)):
                    pip = candidate
                    break
            else:
                module.fail_json(msg=('Unable to find pip in the virtualenv, %s, under any of these names: %s. Make sure pip is present in the virtualenv.' % (env, ', '.join(candidate_pip_basenames))))
    return pip