

def daemonize(module, cmd):
    "\n    Execute a command while detaching as a daemon, returns rc, stdout, and stderr.\n\n    :arg module: is an  AnsibleModule object, used for it's utility methods\n    :arg cmd: is a list or string representing the command and options to run\n\n    This is complex because daemonization is hard for people.\n    What we do is daemonize a part of this module, the daemon runs the command,\n    picks up the return code and output, and returns it to the main process.\n    "
    chunk = 4096
    errors = 'surrogate_or_strict'
    try:
        pipe = os.pipe()
        pid = fork_process()
    except OSError:
        module.fail_json(msg='Error while attempting to fork: %s', exception=traceback.format_exc())
    except Exception as exc:
        module.fail_json(msg=to_text(exc), exception=traceback.format_exc())
    if (pid == 0):
        os.close(pipe[0])
        if (not isinstance(cmd, list)):
            if PY2:
                cmd = shlex.split(to_bytes(cmd, errors=errors))
            else:
                cmd = shlex.split(to_text(cmd, errors=errors))
        run_cmd = []
        for c in cmd:
            run_cmd.append(to_bytes(c, errors=errors))
        p = subprocess.Popen(run_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=(lambda : os.close(pipe[1])))
        fds = [p.stdout, p.stderr]
        output = {
            p.stdout: b(''),
            p.stderr: b(''),
        }
        while fds:
            (rfd, wfd, efd) = select.select(fds, [], fds, 1)
            if (((rfd + wfd) + efd) or p.poll()):
                for out in fds:
                    if (out in rfd):
                        data = os.read(out.fileno(), chunk)
                        if (not data):
                            fds.remove(out)
                    output[out] += b(data)
        p.wait()
        return_data = pickle.dumps([p.returncode, to_text(output[p.stdout]), to_text(output[p.stderr])], protocol=pickle.HIGHEST_PROTOCOL)
        os.write(pipe[1], to_bytes(return_data, errors=errors))
        os.close(pipe[1])
        os._exit(0)
    elif (pid == (- 1)):
        module.fail_json(msg='Unable to fork, no exception thrown, probably due to lack of resources, check logs.')
    else:
        os.close(pipe[1])
        os.waitpid(pid, 0)
        return_data = b('')
        while True:
            (rfd, wfd, efd) = select.select([pipe[0]], [], [pipe[0]])
            if (pipe[0] in rfd):
                data = os.read(pipe[0], chunk)
                if (not data):
                    break
                return_data += b(data)
        return pickle.loads(to_bytes(return_data, errors=errors))
