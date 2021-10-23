

def main():
    module = AnsibleModule(argument_spec=dict(src=dict(type='path', required=True, aliases=['path']), minfw=dict(type='str')))
    changed = True
    src = module.params['src']
    minfw = module.params['minfw']
    options = (' -f %s' % src)
    if minfw:
        options += (' -m %s' % minfw)
    (rc, stdout, stderr) = module.run_command(('hponcfg %s' % options))
    if (rc != 0):
        module.fail_json(rc=rc, msg='Failed to run hponcfg', stdout=stdout, stderr=stderr)
    module.exit_json(changed=changed, stdout=stdout, stderr=stderr)
