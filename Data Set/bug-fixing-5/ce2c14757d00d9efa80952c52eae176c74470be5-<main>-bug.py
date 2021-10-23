def main():
    module = AnsibleModule(argument_spec=dict())
    facter_path = module.get_bin_path('facter', opt_dirs=['/opt/puppetlabs/bin'])
    cmd = [facter_path, '--puppet', '--json']
    (rc, out, err) = module.run_command(cmd, check_rc=True)
    module.exit_json(**json.loads(out))