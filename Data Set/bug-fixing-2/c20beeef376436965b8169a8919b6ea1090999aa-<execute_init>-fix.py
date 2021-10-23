

def execute_init(self):
    '\n        creates the skeleton framework of a role that complies with the galaxy metadata format.\n        '
    init_path = self.options.init_path
    force = self.options.force
    role_skeleton = self.options.role_skeleton
    role_name = (self.args.pop(0).strip() if self.args else None)
    if (not role_name):
        raise AnsibleOptionsError('- no role name specified for init')
    role_path = os.path.join(init_path, role_name)
    if os.path.exists(role_path):
        if os.path.isfile(role_path):
            raise AnsibleError(('- the path %s already exists, but is a file - aborting' % role_path))
        elif (not force):
            raise AnsibleError(('- the directory %s already exists.you can use --force to re-initialize this directory,\nhowever it will reset any main.yml files that may have\nbeen modified there already.' % role_path))
    inject_data = dict(role_name=role_name, author='your name', description='your description', company='your company (optional)', license='license (GPLv2, CC-BY, etc)', issue_tracker_url='http://example.com/issue/tracker', min_ansible_version='1.2', container_enabled=self.options.container_enabled)
    if (not os.path.exists(role_path)):
        os.makedirs(role_path)
    if (role_skeleton is not None):
        skeleton_ignore_expressions = C.GALAXY_ROLE_SKELETON_IGNORE
    else:
        role_skeleton = self.galaxy.default_role_skeleton_path
        skeleton_ignore_expressions = ['^.*/.git_keep$']
    role_skeleton = os.path.expanduser(role_skeleton)
    skeleton_ignore_re = [re.compile(x) for x in skeleton_ignore_expressions]
    template_env = Environment(loader=FileSystemLoader(role_skeleton))
    for (root, dirs, files) in os.walk(role_skeleton, topdown=True):
        rel_root = os.path.relpath(root, role_skeleton)
        in_templates_dir = (rel_root.split(os.sep, 1)[0] == 'templates')
        dirs[:] = [d for d in dirs if (not any((r.match(d) for r in skeleton_ignore_re)))]
        for f in files:
            (filename, ext) = os.path.splitext(f)
            if any((r.match(os.path.join(rel_root, f)) for r in skeleton_ignore_re)):
                continue
            elif ((ext == '.j2') and (not in_templates_dir)):
                src_template = os.path.join(rel_root, f)
                dest_file = os.path.join(role_path, rel_root, filename)
                template_env.get_template(src_template).stream(inject_data).dump(dest_file)
            else:
                f_rel_path = os.path.relpath(os.path.join(root, f), role_skeleton)
                shutil.copyfile(os.path.join(root, f), os.path.join(role_path, f_rel_path))
        for d in dirs:
            dir_path = os.path.join(role_path, rel_root, d)
            if (not os.path.exists(dir_path)):
                os.makedirs(dir_path)
    display.display(('- %s was created successfully' % role_name))
