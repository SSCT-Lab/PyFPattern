def run(self, tmp=None, task_vars=None):
    ' run the pause action module '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    duration_unit = 'minutes'
    prompt = None
    seconds = None
    result.update(dict(changed=False, rc=0, stderr='', stdout='', start=None, stop=None, delta=None))
    if (not (set(self._task.args.keys()) <= set(self.PAUSE_TYPES))):
        result['failed'] = True
        result['msg'] = ('Invalid argument given. Must be one of: %s' % ', '.join((x for x in self.PAUSE_TYPES if (x != ''))))
        return result
    if ('prompt' in self._task.args):
        prompt = ('[%s]\n%s:' % (self._task.get_name().strip(), self._task.args['prompt']))
    else:
        prompt = ('[%s]\n%s:' % (self._task.get_name().strip(), 'Press enter to continue'))
    if (('minutes' in self._task.args) or ('seconds' in self._task.args)):
        try:
            if ('minutes' in self._task.args):
                seconds = (int(self._task.args['minutes']) * 60)
            else:
                seconds = int(self._task.args['seconds'])
                duration_unit = 'seconds'
        except ValueError as e:
            result['failed'] = True
            result['msg'] = ('non-integer value given for prompt duration:\n%s' % to_text(e))
            return result
    start = time.time()
    result['start'] = to_text(datetime.datetime.now())
    result['user_input'] = b''
    fd = None
    old_settings = None
    try:
        if (seconds is not None):
            if (seconds < 1):
                seconds = 1
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            display.display(('Pausing for %d seconds' % seconds))
            (display.display("(ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)\r"),)
            if ('prompt' in self._task.args):
                display.display(prompt)
        else:
            display.display(prompt)
        fd = None
        try:
            if PY3:
                stdin = self._connection._new_stdin.buffer
            else:
                stdin = self._connection._new_stdin
            fd = stdin.fileno()
        except (ValueError, AttributeError):
            stdin = None
        if (fd is not None):
            if isatty(fd):
                old_settings = termios.tcgetattr(fd)
                tty.setraw(fd)
                if (not seconds):
                    new_settings = termios.tcgetattr(fd)
                    new_settings[0] = (new_settings[0] | termios.ICRNL)
                    new_settings[3] = (new_settings[3] | (termios.ICANON | termios.ECHO))
                    termios.tcsetattr(fd, termios.TCSANOW, new_settings)
                    termios.tcsetattr(fd, termios.TCSANOW, new_settings)
                termios.tcflush(stdin, termios.TCIFLUSH)
        while True:
            try:
                if (fd is not None):
                    key_pressed = stdin.read(1)
                    if (key_pressed == b'\x03'):
                        raise KeyboardInterrupt
                if (not seconds):
                    if ((fd is None) or (not isatty(fd))):
                        display.warning('Not waiting from prompt as stdin is not interactive')
                        break
                    if (key_pressed in (b'\r', b'\n')):
                        break
                    else:
                        result['user_input'] += key_pressed
            except KeyboardInterrupt:
                if (seconds is not None):
                    signal.alarm(0)
                (display.display("Press 'C' to continue the play or 'A' to abort \r"),)
                if self._c_or_a(stdin):
                    break
                else:
                    raise AnsibleError('user requested abort!')
    except AnsibleTimeoutExceeded:
        pass
    finally:
        if ((not (None in (fd, old_settings))) and isatty(fd)):
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        duration = (time.time() - start)
        result['stop'] = to_text(datetime.datetime.now())
        result['delta'] = int(duration)
        if (duration_unit == 'minutes'):
            duration = round((duration / 60.0), 2)
        else:
            duration = round(duration, 2)
        result['stdout'] = ('Paused for %s %s' % (duration, duration_unit))
    result['user_input'] = to_text(result['user_input'], errors='surrogate_or_strict')
    return result