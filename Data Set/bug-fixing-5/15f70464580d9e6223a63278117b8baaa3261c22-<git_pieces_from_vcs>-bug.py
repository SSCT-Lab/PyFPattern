@register_vcs_handler('git', 'pieces_from_vcs')
def git_pieces_from_vcs(tag_prefix, root, verbose, run_command=run_command):
    if (not os.path.exists(os.path.join(root, '.git'))):
        if verbose:
            print('no .git in {root}'.format(root=root))
        raise NotThisMethod('no .git directory')
    GITS = ['git']
    if (sys.platform == 'win32'):
        GITS = ['git.cmd', 'git.exe']
    describe_out = run_command(GITS, ['describe', '--tags', '--dirty', '--always', '--long'], cwd=root)
    if (describe_out is None):
        raise NotThisMethod("'git describe' failed")
    describe_out = describe_out.strip()
    full_out = run_command(GITS, ['rev-parse', 'HEAD'], cwd=root)
    if (full_out is None):
        raise NotThisMethod("'git rev-parse' failed")
    full_out = full_out.strip()
    pieces = {
        
    }
    pieces['long'] = full_out
    pieces['short'] = full_out[:7]
    pieces['error'] = None
    git_describe = describe_out
    dirty = git_describe.endswith('-dirty')
    pieces['dirty'] = dirty
    if dirty:
        git_describe = git_describe[:git_describe.rindex('-dirty')]
    if ('-' in git_describe):
        mo = re.search('^(.+)-(\\d+)-g([0-9a-f]+)$', git_describe)
        if (not mo):
            pieces['error'] = "unable to parse git-describe output: '{describe_out}'".format(describe_out=describe_out)
            return pieces
        full_tag = mo.group(1)
        if (not full_tag.startswith(tag_prefix)):
            if verbose:
                fmt = "tag '{full_tag}' doesn't start with prefix '{tag_prefix}'"
                print(fmt.format(full_tag=full_tag, tag_prefix=tag_prefix))
            pieces['error'] = "tag '{full_tag}' doesn't start with prefix '{tag_prefix}'".format(full_tag, tag_prefix)
            return pieces
        pieces['closest-tag'] = full_tag[len(tag_prefix):]
        pieces['distance'] = int(mo.group(2))
        pieces['short'] = mo.group(3)
    else:
        pieces['closest-tag'] = None
        count_out = run_command(GITS, ['rev-list', 'HEAD', '--count'], cwd=root)
        pieces['distance'] = int(count_out)
    return pieces