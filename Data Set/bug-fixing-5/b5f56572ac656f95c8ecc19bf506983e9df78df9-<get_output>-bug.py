def get_output(self, body, headers=None, include_dirs=None, libraries=None, library_dirs=None, lang='c', use_tee=None):
    "Try to compile, link to an executable, and run a program\n        built from 'body' and 'headers'. Returns the exit status code\n        of the program and its output.\n        "
    warnings.warn('\n+++++++++++++++++++++++++++++++++++++++++++++++++\nUsage of get_output is deprecated: please do not \nuse it anymore, and avoid configuration checks \ninvolving running executable on the target machine.\n+++++++++++++++++++++++++++++++++++++++++++++++++\n', DeprecationWarning, stacklevel=2)
    self._check_compiler()
    (exitcode, output) = (255, '')
    try:
        grabber = GrabStdout()
        try:
            (src, obj, exe) = self._link(body, headers, include_dirs, libraries, library_dirs, lang)
            grabber.restore()
        except Exception:
            output = grabber.data
            grabber.restore()
            raise
        exe = os.path.join('.', exe)
        (exitstatus, output) = exec_command(exe, execute_in='.', use_tee=use_tee)
        if hasattr(os, 'WEXITSTATUS'):
            exitcode = os.WEXITSTATUS(exitstatus)
            if os.WIFSIGNALED(exitstatus):
                sig = os.WTERMSIG(exitstatus)
                log.error(('subprocess exited with signal %d' % (sig,)))
                if (sig == signal.SIGINT):
                    raise KeyboardInterrupt
        else:
            exitcode = exitstatus
        log.info('success!')
    except (CompileError, LinkError):
        log.info('failure.')
    self._clean()
    return (exitcode, output)