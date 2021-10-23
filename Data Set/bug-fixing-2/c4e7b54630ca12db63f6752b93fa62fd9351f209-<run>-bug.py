

def run(self, tmp=None, task_vars=None):
    self._supports_check_mode = True
    self._supports_async = True
    if self._play_context.check_mode:
        return dict(changed=True, elapsed=0, rebooted=True)
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp
    if (result.get('skipped', False) or result.get('failed', False)):
        return result
    deprecated_args = {
        'shutdown_timeout': '2.5',
        'shutdown_timeout_sec': '2.5',
    }
    for (arg, version) in deprecated_args.items():
        if (self._task.args.get(arg) is not None):
            display.warning(('Since Ansible %s, %s is no longer used with win_reboot' % (arg, version)))
    if (self._task.args.get('connect_timeout') is not None):
        connect_timeout = int(self._task.args.get('connect_timeout', self.DEFAULT_CONNECT_TIMEOUT))
    else:
        connect_timeout = int(self._task.args.get('connect_timeout_sec', self.DEFAULT_CONNECT_TIMEOUT))
    if (self._task.args.get('reboot_timeout') is not None):
        reboot_timeout = int(self._task.args.get('reboot_timeout', self.DEFAULT_REBOOT_TIMEOUT))
    else:
        reboot_timeout = int(self._task.args.get('reboot_timeout_sec', self.DEFAULT_REBOOT_TIMEOUT))
    if (self._task.args.get('pre_reboot_delay') is not None):
        pre_reboot_delay = int(self._task.args.get('pre_reboot_delay', self.DEFAULT_PRE_REBOOT_DELAY))
    else:
        pre_reboot_delay = int(self._task.args.get('pre_reboot_delay_sec', self.DEFAULT_PRE_REBOOT_DELAY))
    if (self._task.args.get('post_reboot_delay') is not None):
        post_reboot_delay = int(self._task.args.get('post_reboot_delay', self.DEFAULT_POST_REBOOT_DELAY))
    else:
        post_reboot_delay = int(self._task.args.get('post_reboot_delay_sec', self.DEFAULT_POST_REBOOT_DELAY))
    test_command = str(self._task.args.get('test_command', self.DEFAULT_TEST_COMMAND))
    msg = str(self._task.args.get('msg', self.DEFAULT_REBOOT_MESSAGE))
    try:
        before_uptime = self.get_system_uptime()
    except Exception as e:
        result['failed'] = True
        result['reboot'] = False
        result['msg'] = to_native(e)
        return result
    display.vvv('rebooting server')
    (rc, stdout, stderr) = self._connection.exec_command(('shutdown /r /t %d /c "%s"' % (pre_reboot_delay, msg)))
    if (rc == 1190):
        display.warning('A scheduled reboot was pre-empted by Ansible.')
        (rc, stdout1, stderr1) = self._connection.exec_command('shutdown /a')
        (rc, stdout2, stderr2) = self._connection.exec_command(('shutdown /r /t %d' % pre_reboot_delay))
        stdout += (stdout1 + stdout2)
        stderr += (stderr1 + stderr2)
    if (rc != 0):
        result['failed'] = True
        result['rebooted'] = False
        result['msg'] = ('Shutdown command failed, error text was %s' % stderr)
        return result
    start = datetime.now()
    connection_timeout_orig = None
    try:
        connection_timeout_orig = self._connection.get_option('connection_timeout')
    except AnsibleError:
        display.debug('win_reboot: connection_timeout connection option has not been set')
    try:

        def check_uptime():
            display.vvv('attempting to get system uptime')
            try:
                self._connection.set_options(direct={
                    'connection_timeout': connect_timeout,
                })
                self._connection._reset()
            except AttributeError:
                display.warning('Connection plugin does not allow the connection timeout to be overridden')
            try:
                current_uptime = self.get_system_uptime()
            except Exception as e:
                raise e
            if (current_uptime == before_uptime):
                raise Exception('uptime has not changed')
        self.do_until_success_or_timeout(check_uptime, reboot_timeout, what_desc='reboot uptime check success')
        try:
            self._connection.set_options(direct={
                'connection_timeout': connection_timeout_orig,
            })
            self._connection._reset()
        except (AnsibleError, AttributeError):
            display.debug('Failed to reset connection_timeout back to default')

        def run_test_command():
            display.vvv(("attempting post-reboot test command '%s'" % test_command))
            (rc, stdout, stderr) = self._connection.exec_command(test_command)
            if (rc != 0):
                raise Exception('test command failed')
        self.do_until_success_or_timeout(run_test_command, reboot_timeout, what_desc='post-reboot test command success')
        result['rebooted'] = True
        result['changed'] = True
    except TimedOutException as toex:
        result['failed'] = True
        result['rebooted'] = True
        result['msg'] = to_native(toex)
    if (post_reboot_delay != 0):
        display.vvv(('win_reboot: waiting an additional %d seconds' % post_reboot_delay))
        time.sleep(post_reboot_delay)
    elapsed = (datetime.now() - start)
    result['elapsed'] = elapsed.seconds
    return result
