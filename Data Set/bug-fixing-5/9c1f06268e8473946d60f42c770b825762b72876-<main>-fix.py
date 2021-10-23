def main():
    module = AnsibleModule(argument_spec=dict(commandfile=dict(required=True), outputfile=dict(required=True), condition=dict(required=True), flag=dict(required=True), host=dict(required=True), deviceType=dict(required=True), username=dict(required=True), password=dict(required=True, no_log=True), enablePassword=dict(required=False, no_log=True)), supports_check_mode=False)
    condition = module.params['condition']
    flag = module.params['flag']
    commandfile = module.params['commandfile']
    outputfile = module.params['outputfile']
    output = ''
    if ((condition is None) or (condition != flag)):
        module.exit_json(changed=True, msg='Template Skipped for this switch')
        return ' '
    f = open(commandfile, 'r')
    cmd = []
    for line in f:
        if (not line.startswith('#')):
            command = line.strip()
            inner_cmd = [{
                'command': command,
                'prompt': None,
                'answer': None,
            }]
            cmd.extend(inner_cmd)
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
        module.exit_json(changed=True, msg='Template Applied')
    else:
        module.fail_json(msg=errorMsg)