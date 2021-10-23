

def _ssh_retry(func):
    '\n    Decorator to retry ssh/scp/sftp in the case of a connection failure\n\n    Will retry if:\n    * an exception is caught\n    * ssh returns 255\n    Will not retry if\n    * remaining_tries is <2\n    * retries limit reached\n    '

    @wraps(func)
    def wrapped(self, *args, **kwargs):
        remaining_tries = (int(C.ANSIBLE_SSH_RETRIES) + 1)
        cmd_summary = ('%s...' % args[0])
        for attempt in range(remaining_tries):
            cmd = args[0]
            if ((attempt != 0) and self._play_context.password and isinstance(cmd, list)):
                self.sshpass_pipe = os.pipe()
                cmd[1] = (b'-d' + to_bytes(self.sshpass_pipe[0], nonstring='simplerepr', errors='surrogate_or_strict'))
            try:
                try:
                    return_tuple = func(self, *args, **kwargs)
                    display.vvv(return_tuple, host=self.host)
                except AnsibleControlPersistBrokenPipeError as e:
                    display.vvv('RETRYING BECAUSE OF CONTROLPERSIST BROKEN PIPE')
                    return_tuple = func(self, *args, **kwargs)
                if (return_tuple[0] != 255):
                    break
                else:
                    raise AnsibleConnectionFailure(('Failed to connect to the host via ssh: %s' % to_native(return_tuple[2])))
            except (AnsibleConnectionFailure, Exception) as e:
                if (attempt == (remaining_tries - 1)):
                    raise
                else:
                    pause = ((2 ** attempt) - 1)
                    if (pause > 30):
                        pause = 30
                    if isinstance(e, AnsibleConnectionFailure):
                        msg = ('ssh_retry: attempt: %d, ssh return code is 255. cmd (%s), pausing for %d seconds' % (attempt, cmd_summary, pause))
                    else:
                        msg = ('ssh_retry: attempt: %d, caught exception(%s) from cmd (%s), pausing for %d seconds' % (attempt, e, cmd_summary, pause))
                    display.vv(msg, host=self.host)
                    time.sleep(pause)
                    continue
        return return_tuple
    return wrapped
