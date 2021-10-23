def main():
    module = AnsibleModule(argument_spec=dict(service_path=dict(required=True), state=dict(default='present', choices=['present', 'absent'], required=False), functions=dict(type='list', required=False), region=dict(default='', required=False), stage=dict(default='', required=False), deploy=dict(default=True, type='bool', required=False)))
    service_path = os.path.expanduser(module.params.get('service_path'))
    state = module.params.get('state')
    functions = module.params.get('functions')
    region = module.params.get('region')
    stage = module.params.get('stage')
    deploy = module.params.get('deploy', True)
    command = 'serverless '
    if (state == 'present'):
        command += 'deploy '
    elif (state == 'absent'):
        command += 'remove '
    else:
        module.fail_json(msg="State must either be 'present' or 'absent'. Received: {}".format(state))
    if ((not deploy) and (state == 'present')):
        command += '--noDeploy '
    if region:
        command += '--region {} '.format(region)
    if stage:
        command += '--stage {} '.format(stage)
    (rc, out, err) = module.run_command(command, cwd=service_path)
    if (rc != 0):
        if ((state == 'absent') and ("-{}' does not exist".format(stage) in out)):
            module.exit_json(changed=False, state='absent', command=command, out=out, service_name=get_service_name(module, stage))
        module.fail_json(msg='Failure when executing Serverless command. Exited {}.\nstdout: {}\nstderr: {}'.format(rc, out, err))
    module.exit_json(changed=True, state='present', out=out, command=command, service_name=get_service_name(module, stage))