@magic_arguments.magic_arguments()
@script_args
@cell_magic('script')
def shebang(self, line, cell):
    'Run a cell via a shell command\n        \n        The `%%script` line is like the #! line of script,\n        specifying a program (bash, perl, ruby, etc.) with which to run.\n        \n        The rest of the cell is run by that program.\n        \n        Examples\n        --------\n        ::\n        \n            In [1]: %%script bash\n               ...: for i in 1 2 3; do\n               ...:   echo $i\n               ...: done\n            1\n            2\n            3\n        '
    argv = arg_split(line, posix=(not sys.platform.startswith('win')))
    (args, cmd) = self.shebang.parser.parse_known_args(argv)
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    except OSError as e:
        if (e.errno == errno.ENOENT):
            print(("Couldn't find program: %r" % cmd[0]))
            return
        else:
            raise
    if (not cell.endswith('\n')):
        cell += '\n'
    cell = cell.encode('utf8', 'replace')
    if args.bg:
        self.bg_processes.append(p)
        self._gc_bg_processes()
        to_close = []
        if args.out:
            self.shell.user_ns[args.out] = p.stdout
        else:
            to_close.append(p.stdout)
        if args.err:
            self.shell.user_ns[args.err] = p.stderr
        else:
            to_close.append(p.stderr)
        self.job_manager.new(self._run_script, p, cell, to_close, daemon=True)
        if args.proc:
            self.shell.user_ns[args.proc] = p
        return
    try:
        (out, err) = p.communicate(cell)
    except KeyboardInterrupt:
        try:
            p.send_signal(signal.SIGINT)
            time.sleep(0.1)
            if (p.poll() is not None):
                print('Process is interrupted.')
                return
            p.terminate()
            time.sleep(0.1)
            if (p.poll() is not None):
                print('Process is terminated.')
                return
            p.kill()
            print('Process is killed.')
        except OSError:
            pass
        except Exception as e:
            print(('Error while terminating subprocess (pid=%i): %s' % (p.pid, e)))
        return
    out = py3compat.decode(out)
    err = py3compat.decode(err)
    if args.out:
        self.shell.user_ns[args.out] = out
    else:
        sys.stdout.write(out)
        sys.stdout.flush()
    if args.err:
        self.shell.user_ns[args.err] = err
    else:
        sys.stderr.write(err)
        sys.stderr.flush()
    if (args.raise_error and (p.returncode != 0)):
        raise CalledProcessError(p.returncode, cell, output=out, stderr=err)