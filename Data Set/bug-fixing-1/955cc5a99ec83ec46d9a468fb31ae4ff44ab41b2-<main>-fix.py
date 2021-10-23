

def main():
    module = AnsibleModule(argument_spec=dict(src=dict(type='path', required=True, aliases=['path']), minfw=dict(type='str'), executable=dict(default='hponcfg', type='str'), verbose=dict(default=False, type='bool')))
    changed = True
    src = module.params['src']
    minfw = module.params['minfw']
    executable = module.params['executable']
    verbose = module.params['verbose']
    options = (' -f %s' % src)
    if verbose:
        options += ' -v'
    if minfw:
        options += (' -m %s' % minfw)
    (rc, stdout, stderr) = module.run_command(('%s %s' % (executable, options)))
    if (rc != 0):
        module.fail_json(rc=rc, msg='Failed to run hponcfg', stdout=stdout, stderr=stderr)
    module.exit_json(changed=changed, stdout=stdout, stderr=stderr)
