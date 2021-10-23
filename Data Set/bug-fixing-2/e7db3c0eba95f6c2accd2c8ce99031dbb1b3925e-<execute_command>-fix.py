

def execute_command(self, cmd, daemonize=False):
    if (not daemonize):
        return self.module.run_command(cmd)
    pipe = os.pipe()
    pid = os.fork()
    if (pid == 0):
        os.close(pipe[0])
        fd = os.open(os.devnull, os.O_RDWR)
        if (fd != 0):
            os.dup2(fd, 0)
        if (fd != 1):
            os.dup2(fd, 1)
        if (fd != 2):
            os.dup2(fd, 2)
        if (fd not in (0, 1, 2)):
            os.close(fd)
        pid = os.fork()
        if (pid > 0):
            os._exit(0)
        os.setsid()
        os.chdir('/')
        pid = os.fork()
        if (pid > 0):
            os._exit(0)
        if PY2:
            cmd = to_bytes(cmd, errors='surrogate_or_strict')
            cmd = shlex.split(cmd)
        else:
            cmd = to_text(cmd, errors='surrogate_or_strict')
            cmd = [to_bytes(c, errors='surrogate_or_strict') for c in shlex.split(cmd)]
        lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=lang_env, preexec_fn=(lambda : os.close(pipe[1])))
        stdout = b('')
        stderr = b('')
        fds = [p.stdout, p.stderr]
        while fds:
            (rfd, wfd, efd) = select.select(fds, [], fds, 1)
            if ((not ((rfd + wfd) + efd)) and (p.poll() is not None)):
                break
            if (p.stdout in rfd):
                dat = os.read(p.stdout.fileno(), 4096)
                if (not dat):
                    fds.remove(p.stdout)
                stdout += dat
            if (p.stderr in rfd):
                dat = os.read(p.stderr.fileno(), 4096)
                if (not dat):
                    fds.remove(p.stderr)
                stderr += dat
        p.wait()
        blob = json.dumps([p.returncode, to_text(stdout), to_text(stderr)])
        os.write(pipe[1], to_bytes(blob, errors='surrogate_or_strict'))
        os.close(pipe[1])
        os._exit(0)
    elif (pid == (- 1)):
        self.module.fail_json(msg='unable to fork')
    else:
        os.close(pipe[1])
        os.waitpid(pid, 0)
        data = b('')
        while True:
            (rfd, wfd, efd) = select.select([pipe[0]], [], [pipe[0]])
            if (pipe[0] in rfd):
                dat = os.read(pipe[0], 4096)
                if (not dat):
                    break
                data += dat
        return json.loads(to_text(data, errors='surrogate_or_strict'))
