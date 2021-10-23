def main():
    module = AnsibleModule(argument_spec=dict(commandfile=dict(required=True), outputfile=dict(required=True), condition=dict(required=True), flag=dict(required=True), host=dict(required=True), deviceType=dict(required=True), username=dict(required=True), password=dict(required=True, no_log=True), enablePassword=dict(required=False, no_log=True)), supports_check_mode=False)
    username = module.params['username']
    password = module.params['password']
    enablePassword = module.params['enablePassword']
    condition = module.params['condition']
    flag = module.params['flag']
    commandfile = module.params['commandfile']
    deviceType = module.params['deviceType']
    outputfile = module.params['outputfile']
    hostIP = module.params['host']
    output = ''
    if (not HAS_PARAMIKO):
        module.fail_json(msg='paramiko is required for this module')
    if (condition != flag):
        module.exit_json(changed=True, msg='Template Skipped for this value')
        return ' '
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(hostIP, username=username, password=password)
    time.sleep(2)
    remote_conn = remote_conn_pre.invoke_shell()
    time.sleep(2)
    output = (output + cnos.waitForDeviceResponse('\n', '>', 2, remote_conn))
    output = (output + cnos.enterEnableModeForDevice(enablePassword, 3, remote_conn))
    output = (output + cnos.waitForDeviceResponse('terminal length 0\n', '#', 2, remote_conn))
    output = (output + cnos.waitForDeviceResponse('configure device\n', '(config)#', 2, remote_conn))
    f = open(commandfile, 'r')
    for line in f:
        if (not line.startswith('#')):
            command = line
            if (not line.endswith('\n')):
                command = (command + '\n')
            response = cnos.waitForDeviceResponse(command, '#', 2, remote_conn)
            errorMsg = cnos.checkOutputForError(response)
            output = (output + response)
            if (errorMsg is not None):
                break
    output = (output + cnos.waitForDeviceResponse('save\n', '#', 3, remote_conn))
    file = open(outputfile, 'a')
    file.write(output)
    file.close()
    errorMsg = cnos.checkOutputForError(output)
    if (errorMsg is None):
        module.exit_json(changed=True, msg='Template Applied')
    else:
        module.fail_json(msg=errorMsg)