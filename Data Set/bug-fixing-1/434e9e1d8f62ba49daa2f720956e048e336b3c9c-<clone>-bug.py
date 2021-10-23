

def clone(git_path, module, repo, dest, remote, depth, version, bare, reference, refspec, verify_commit):
    ' makes a new git repo if it does not already exist '
    dest_dirname = os.path.dirname(dest)
    try:
        os.makedirs(dest_dirname)
    except:
        pass
    cmd = [git_path, 'clone']
    if bare:
        cmd.append('--bare')
    else:
        cmd.extend(['--origin', remote])
    if depth:
        if ((version == 'HEAD') or refspec):
            cmd.extend(['--depth', str(depth)])
        elif (is_remote_branch(git_path, module, dest, repo, version) or is_remote_tag(git_path, module, dest, repo, version)):
            cmd.extend(['--depth', str(depth)])
            cmd.extend(['--branch', version])
        else:
            module.warn('Ignoring depth argument. Shallow clones are only available for HEAD, branches, tags or in combination with refspec.')
    if reference:
        cmd.extend(['--reference', str(reference)])
    cmd.extend([repo, dest])
    module.run_command(cmd, check_rc=True, cwd=dest_dirname)
    if bare:
        if (remote != 'origin'):
            module.run_command([git_path, 'remote', 'add', remote, repo], check_rc=True, cwd=dest)
    if refspec:
        cmd = [git_path, 'fetch']
        if depth:
            cmd.extend(['--depth', str(depth)])
        cmd.extend([remote, refspec])
        module.run_command(cmd, check_rc=True, cwd=dest)
    if verify_commit:
        verify_commit_sign(git_path, module, dest, version)
