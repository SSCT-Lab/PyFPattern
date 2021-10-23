def main():
    module = AnsibleModule(argument_spec=dict(timeout=dict(default='30m'), puppetmaster=dict(required=False, default=None), modulepath=dict(required=False, default=None), manifest=dict(required=False, default=None), logdest=dict(required=False, default='stdout', choices=['stdout', 'syslog']), show_diff=dict(default=False, aliases=['show-diff'], type='bool'), facts=dict(default=None), facter_basename=dict(default='ansible'), environment=dict(required=False, default=None), certname=dict(required=False, default=None), tags=dict(required=False, default=None, type='list'), execute=dict(required=False, default=None)), supports_check_mode=True, mutually_exclusive=[('puppetmaster', 'manifest'), ('puppetmaster', 'manifest', 'execute'), ('puppetmaster', 'modulepath')])
    p = module.params
    global PUPPET_CMD
    PUPPET_CMD = module.get_bin_path('puppet', False, ['/opt/puppetlabs/bin'])
    if (not PUPPET_CMD):
        module.fail_json(msg='Could not find puppet. Please ensure it is installed.')
    global TIMEOUT_CMD
    TIMEOUT_CMD = module.get_bin_path('timeout', False)
    if p['manifest']:
        if (not os.path.exists(p['manifest'])):
            module.fail_json(msg=('Manifest file %(manifest)s not found.' % dict(manifest=p['manifest'])))
    if (not p['manifest']):
        (rc, stdout, stderr) = module.run_command((PUPPET_CMD + ' config print agent_disabled_lockfile'))
        if os.path.exists(stdout.strip()):
            module.fail_json(msg='Puppet agent is administratively disabled.', disabled=True)
        elif (rc != 0):
            module.fail_json(msg='Puppet agent state could not be determined.')
    if (module.params['facts'] and (not module.check_mode)):
        _write_structured_data(_get_facter_dir(), module.params['facter_basename'], module.params['facts'])
    if TIMEOUT_CMD:
        base_cmd = ('%(timeout_cmd)s -s 9 %(timeout)s %(puppet_cmd)s' % dict(timeout_cmd=TIMEOUT_CMD, timeout=pipes.quote(p['timeout']), puppet_cmd=PUPPET_CMD))
    else:
        base_cmd = PUPPET_CMD
    if (not p['manifest']):
        cmd = ('%(base_cmd)s agent --onetime --ignorecache --no-daemonize --no-usecacheonfailure --no-splay --detailed-exitcodes --verbose --color 0' % dict(base_cmd=base_cmd))
        if p['puppetmaster']:
            cmd += (' --server %s' % pipes.quote(p['puppetmaster']))
        if p['show_diff']:
            cmd += ' --show_diff'
        if p['environment']:
            cmd += (" --environment '%s'" % p['environment'])
        if p['tags']:
            cmd += (" --tags '%s'" % ','.join(p['tags']))
        if p['certname']:
            cmd += (" --certname='%s'" % p['certname'])
        if module.check_mode:
            cmd += ' --noop'
        else:
            cmd += ' --no-noop'
    else:
        cmd = ('%s apply --detailed-exitcodes ' % base_cmd)
        if (p['logdest'] == 'syslog'):
            cmd += '--logdest syslog '
        if p['modulepath']:
            cmd += ("--modulepath='%s'" % p['modulepath'])
        if p['environment']:
            cmd += ("--environment '%s' " % p['environment'])
        if p['certname']:
            cmd += (" --certname='%s'" % p['certname'])
        if p['execute']:
            cmd += (" --execute '%s'" % p['execute'])
        if p['tags']:
            cmd += (" --tags '%s'" % ','.join(p['tags']))
        if module.check_mode:
            cmd += '--noop '
        else:
            cmd += '--no-noop '
        cmd += pipes.quote(p['manifest'])
    (rc, stdout, stderr) = module.run_command(cmd)
    if (rc == 0):
        module.exit_json(rc=rc, changed=False, stdout=stdout, stderr=stderr)
    elif (rc == 1):
        disabled = ('administratively disabled' in stdout)
        if disabled:
            msg = 'puppet is disabled'
        else:
            msg = 'puppet did not run'
        module.exit_json(rc=rc, disabled=disabled, msg=msg, error=True, stdout=stdout, stderr=stderr)
    elif (rc == 2):
        module.exit_json(rc=0, changed=True, stdout=stdout, stderr=stderr)
    elif (rc == 124):
        module.exit_json(rc=rc, msg=('%s timed out' % cmd), stdout=stdout, stderr=stderr)
    else:
        module.fail_json(rc=rc, msg=('%s failed with return code: %d' % (cmd, rc)), stdout=stdout, stderr=stderr)