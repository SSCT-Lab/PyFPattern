

def configure(src_base_path, gen_path, debug=False):
    'Configure `src_base_path` to embed git hashes if available.'
    git_path = os.path.join(src_base_path, '.git')
    if os.path.exists(gen_path):
        if os.path.isdir(gen_path):
            try:
                shutil.rmtree(gen_path)
            except OSError:
                raise RuntimeError(('Cannot delete directory %s due to permission error, inspect and remove manually' % gen_path))
        else:
            raise RuntimeError('Cannot delete non-directory %s, inspect ', ('and remove manually' % gen_path))
    os.makedirs(gen_path)
    if (not os.path.isdir(gen_path)):
        raise RuntimeError('gen_git_source.py: Failed to create dir')
    spec = {
        
    }
    link_map = {
        'head': None,
        'branch_ref': None,
    }
    if (not os.path.isdir(git_path)):
        spec['git'] = False
        open(os.path.join(gen_path, 'head'), 'w').write('')
        open(os.path.join(gen_path, 'branch_ref'), 'w').write('')
    else:
        spec['git'] = True
        spec['path'] = src_base_path
        git_head_path = os.path.join(git_path, 'HEAD')
        spec['branch'] = parse_branch_ref(git_head_path)
        link_map['head'] = git_head_path
        if (spec['branch'] is not None):
            link_map['branch_ref'] = os.path.join(git_path, *os.path.split(spec['branch']))
    for (target, src) in link_map.items():
        if (src is None):
            open(os.path.join(gen_path, target), 'w').write('')
        else:
            try:
                if hasattr(os, 'symlink'):
                    os.symlink(src, os.path.join(gen_path, target))
                else:
                    shutil.copy2(src, os.path.join(gen_path, target))
            except OSError:
                shutil.copy2(src, os.path.join(gen_path, target))
    json.dump(spec, open(os.path.join(gen_path, 'spec.json'), 'w'), indent=2)
    if debug:
        print(('gen_git_source.py: list %s' % gen_path))
        print(('gen_git_source.py: %s' + repr(os.listdir(gen_path))))
        print(('gen_git_source.py: spec is %r' % spec))
