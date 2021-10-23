

def main():
    module = AnsibleModule(argument_spec=dict(outputfile=dict(required=True), host=dict(required=True), username=dict(required=True), password=dict(required=True, no_log=True), enablePassword=dict(required=False, no_log=True), deviceType=dict(required=True)), supports_check_mode=False)
    username = module.params['username']
    password = module.params['password']
    enablePassword = module.params['enablePassword']
    cliCommand = 'reload \n'
    outputfile = module.params['outputfile']
    hostIP = module.params['host']
    deviceType = module.params['deviceType']
    output = ''
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(hostIP, username=username, password=password)
    time.sleep(2)
    remote_conn = remote_conn_pre.invoke_shell()
    time.sleep(2)
    output = (output + cnos.waitForDeviceResponse('\n', '>', 2, remote_conn))
    output = (output + cnos.enterEnableModeForDevice(enablePassword, 3, remote_conn))
    output = (output + cnos.waitForDeviceResponse('terminal length 0\n', '#', 2, remote_conn))
    output = (output + cnos.waitForDeviceResponse(cliCommand, '(y/n):', 2, remote_conn))
    output = (output + cnos.waitForDeviceResponse('y\n', '#', 2, remote_conn))
    file = open(outputfile, 'a')
    file.write(output)
    file.close()
    errorMsg = cnos.checkOutputForError(output)
    if (errorMsg in 'Device Response Timed out'):
        module.exit_json(changed=True, msg='Device is Reloading. Please wait...')
    else:
        module.fail_json(msg=errorMsg)
