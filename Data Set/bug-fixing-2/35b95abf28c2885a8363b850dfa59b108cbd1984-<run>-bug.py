

def run(self):
    ' use Runner lib to do SSH things '
    super(PullCLI, self).run()
    now = datetime.datetime.now()
    display.display(now.strftime('Starting Ansible Pull at %F %T'))
    display.display(' '.join(sys.argv))
    node = platform.node()
    host = socket.getfqdn()
    limit_opts = ('localhost,%s,127.0.0.1' % ','.join(set([host, node, host.split('.')[0], node.split('.')[0]])))
    base_opts = '-c local '
    if (context.CLIARGS['verbosity'] > 0):
        base_opts += (' -%s' % ''.join(['v' for x in range(0, context.CLIARGS['verbosity'])]))
    inv_opts = self._get_inv_cli()
    if (not inv_opts):
        inv_opts = ' -i localhost, '
    if (context.CLIARGS['module_name'] == 'git'):
        repo_opts = ('name=%s dest=%s' % (context.CLIARGS['url'], context.CLIARGS['dest']))
        if context.CLIARGS['checkout']:
            repo_opts += (' version=%s' % context.CLIARGS['checkout'])
        if context.CLIARGS['accept_host_key']:
            repo_opts += ' accept_hostkey=yes'
        if context.CLIARGS['private_key_file']:
            repo_opts += (' key_file=%s' % context.CLIARGS['private_key_file'])
        if context.CLIARGS['verify']:
            repo_opts += ' verify_commit=yes'
        if context.CLIARGS['tracksubs']:
            repo_opts += ' track_submodules=yes'
        if (not context.CLIARGS['fullclone']):
            repo_opts += ' depth=1'
    elif (context.CLIARGS['module_name'] == 'subversion'):
        repo_opts = ('repo=%s dest=%s' % (context.CLIARGS['url'], context.CLIARGS['dest']))
        if context.CLIARGS['checkout']:
            repo_opts += (' revision=%s' % context.CLIARGS['checkout'])
        if (not context.CLIARGS['fullclone']):
            repo_opts += ' export=yes'
    elif (context.CLIARGS['module_name'] == 'hg'):
        repo_opts = ('repo=%s dest=%s' % (context.CLIARGS['url'], context.CLIARGS['dest']))
        if context.CLIARGS['checkout']:
            repo_opts += (' revision=%s' % context.CLIARGS['checkout'])
    elif (context.CLIARGS['module_name'] == 'bzr'):
        repo_opts = ('name=%s dest=%s' % (context.CLIARGS['url'], context.CLIARGS['dest']))
        if context.CLIARGS['checkout']:
            repo_opts += (' version=%s' % context.CLIARGS['checkout'])
    else:
        raise AnsibleOptionsError(('Unsupported (%s) SCM module for pull, choices are: %s' % (context.CLIARGS['module_name'], ','.join(self.REPO_CHOICES))))
    if context.CLIARGS['clean']:
        repo_opts += ' force=yes'
    path = module_loader.find_plugin(context.CLIARGS['module_name'])
    if (path is None):
        raise AnsibleOptionsError(("module '%s' not found.\n" % context.CLIARGS['module_name']))
    bin_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    cmd = ('%s/ansible %s %s -m %s -a "%s" all -l "%s"' % (bin_path, inv_opts, base_opts, context.CLIARGS['module_name'], repo_opts, limit_opts))
    for ev in context.CLIARGS['extra_vars']:
        cmd += (' -e %s' % shlex_quote(ev))
    if context.CLIARGS['sleep']:
        display.display(('Sleeping for %d seconds...' % context.CLIARGS['sleep']))
        time.sleep(context.CLIARGS['sleep'])
    display.debug('running ansible with VCS module to checkout repo')
    display.vvvv(('EXEC: %s' % cmd))
    (rc, b_out, b_err) = run_cmd(cmd, live=True)
    if (rc != 0):
        if context.CLIARGS['force']:
            display.warning('Unable to update repository. Continuing with (forced) run of playbook.')
        else:
            return rc
    elif (context.CLIARGS['ifchanged'] and (b'"changed": true' not in b_out)):
        display.display('Repository has not changed, quitting.')
        return 0
    playbook = self.select_playbook(context.CLIARGS['dest'])
    if (playbook is None):
        raise AnsibleOptionsError('Could not find a playbook to run.')
    cmd = ('%s/ansible-playbook %s %s' % (bin_path, base_opts, playbook))
    if context.CLIARGS['vault_password_files']:
        for vault_password_file in context.CLIARGS['vault_password_files']:
            cmd += (' --vault-password-file=%s' % vault_password_file)
    if context.CLIARGS['vault_ids']:
        for vault_id in context.CLIARGS['vault_ids']:
            cmd += (' --vault-id=%s' % vault_id)
    for ev in context.CLIARGS['extra_vars']:
        cmd += (' -e %s' % shlex_quote(ev))
    if context.CLIARGS['become_ask_pass']:
        cmd += ' --ask-become-pass'
    if context.CLIARGS['skip_tags']:
        cmd += (' --skip-tags "%s"' % to_native(','.join(context.CLIARGS['skip_tags'])))
    if context.CLIARGS['tags']:
        cmd += (' -t "%s"' % to_native(','.join(context.CLIARGS['tags'])))
    if context.CLIARGS['subset']:
        cmd += (' -l "%s"' % context.CLIARGS['subset'])
    else:
        cmd += (' -l "%s"' % limit_opts)
    if context.CLIARGS['check']:
        cmd += ' -C'
    if context.CLIARGS['diff']:
        cmd += ' -D'
    os.chdir(context.CLIARGS['dest'])
    inv_opts = self._get_inv_cli()
    if inv_opts:
        cmd += inv_opts
    display.debug('running ansible-playbook to do actual work')
    display.debug(('EXEC: %s' % cmd))
    (rc, b_out, b_err) = run_cmd(cmd, live=True)
    if context.CLIARGS['purge']:
        os.chdir('/')
        try:
            shutil.rmtree(context.CLIARGS['dest'])
        except Exception as e:
            display.error(('Failed to remove %s: %s' % (context.CLIARGS['dest'], to_text(e))))
    return rc
