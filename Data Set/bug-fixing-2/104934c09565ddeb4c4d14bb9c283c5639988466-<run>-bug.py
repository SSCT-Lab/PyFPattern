

def run(self, tmp=None, task_vars=None):
    ' run the pause action module '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    duration_unit = 'minutes'
    prompt = None
    seconds = None
    result.update(dict(changed=False, rc=0, stderr='', stdout='', start=None, stop=None, delta=None))
    if ((self._task.args is None) or (len(self._task.args.keys()) == 0)):
        prompt = ('[%s]\nPress enter to continue:' % self._task.get_name().strip())
    elif (('minutes' in self._task.args) or ('seconds' in self._task.args)):
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
    elif ('prompt' in self._task.args):
        prompt = ('[%s]\n%s:' % (self._task.get_name().strip(), self._task.args['prompt']))
    else:
        result['failed'] = True
        result['msg'] = ('invalid pause type given. must be one of: %s' % ', '.join(self.PAUSE_TYPES))
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
        else:
            display.display(prompt)
        if PY3:
            stdin = self._connection._new_stdin.buffer
        else:
            stdin = self._connection._new_stdin
        fd = None
        try:
            fd = stdin.fileno()
        except (ValueError, AttributeError):
            pass
        if (fd is not None):
            if isatty(fd):
                old_settings = termios.tcgetattr(fd)
                tty.setraw(fd)
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
