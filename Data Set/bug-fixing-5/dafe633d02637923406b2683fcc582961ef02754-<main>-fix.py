def main():
    module = AnsibleModule(argument_spec=dict(clicommand=dict(required=True), outputfile=dict(required=True), condition=dict(required=True), flag=dict(required=True), host=dict(required=True), deviceType=dict(required=True), username=dict(required=True), password=dict(required=True, no_log=True), enablePassword=dict(required=False, no_log=True)), supports_check_mode=False)
    condition = module.params['condition']
    flag = module.params['flag']
    cliCommand = module.params['clicommand']
    outputfile = module.params['outputfile']
    output = ''
    if ((condition is None) or (condition != flag)):
        module.exit_json(changed=True, msg='Command Skipped for this switch')
        return ''
    cmd = [{
        'command': cliCommand,
        'prompt': None,
        'answer': None,
    }]
    output = (output + str(cnos.run_cnos_commands(module, cmd)))
    save_cmd = [{
        'command': 'save',
        'prompt': None,
        'answer': None,
    }]
    cmd.extend(save_cmd)
    output = (output + str(cnos.run_cnos_commands(module, cmd)))
    path = outputfile.rsplit('/', 1)
    if (not os.path.exists(path[0])):
        os.makedirs(path[0])
    file = open(outputfile, 'a')
    file.write(output)
    file.close()
    errorMsg = cnos.checkOutputForError(output)
    if (errorMsg is None):
        module.exit_json(changed=True, msg='CLI Command executed and results saved in file ')
    else:
        module.fail_json(msg=errorMsg)