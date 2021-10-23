def main():
    module = AnsibleModule(argument_spec=dict(clicommand=dict(required=True), outputfile=dict(required=True), condition=dict(required=True), flag=dict(required=True), host=dict(required=True), deviceType=dict(required=True), username=dict(required=True), password=dict(required=True, no_log=True), enablePassword=dict(required=False, no_log=True)), supports_check_mode=False)
    username = module.params['username']
    password = module.params['password']
    enablePassword = module.params['enablePassword']
    condition = module.params['condition']
    flag = module.params['flag']
    cliCommand = module.params['clicommand']
    outputfile = module.params['outputfile']
    deviceType = module.params['deviceType']
    hostIP = module.params['host']
    output = ''
    if (not HAS_PARAMIKO):
        module.fail_json(msg='paramiko is required for this module')
    if (condition != flag):
        module.exit_json(changed=True, msg='Command Skipped for this value')
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
    output = (output + cnos.waitForDeviceResponse((cliCommand + '\n'), '(config)#', 2, remote_conn))
    file = open(outputfile, 'a')
    file.write(output)
    file.close()
    errorMsg = cnos.checkOutputForError(output)
    if (errorMsg is None):
        module.exit_json(changed=True, msg='CLI Command executed and results saved in file ')
    else:
        module.fail_json(msg=errorMsg)