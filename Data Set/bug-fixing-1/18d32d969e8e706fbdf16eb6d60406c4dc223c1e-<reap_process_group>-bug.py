

def reap_process_group(pid, log, sig=signal.SIGTERM, timeout=DEFAULT_TIME_TO_WAIT_AFTER_SIGTERM):
    '\n    Tries really hard to terminate all children (including grandchildren). Will send\n    sig (SIGTERM) to the process group of pid. If any process is alive after timeout\n    a SIGKILL will be send.\n\n    :param log: log handler\n    :param pid: pid to kill\n    :param sig: signal type\n    :param timeout: how much time a process has to terminate\n    '

    def on_terminate(p):
        log.info('Process %s (%s) terminated with exit code %s', p, p.pid, p.returncode)
    if (pid == os.getpid()):
        raise RuntimeError('I refuse to kill myself')
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    children.append(parent)
    try:
        pg = os.getpgid(pid)
    except OSError as err:
        if (err.errno == errno.ESRCH):
            return
        raise
    log.info('Sending %s to GPID %s', sig, pg)
    os.killpg(os.getpgid(pid), sig)
    (_, alive) = psutil.wait_procs(children, timeout=timeout, callback=on_terminate)
    if alive:
        for p in alive:
            log.warn('process %s (%s) did not respond to SIGTERM. Trying SIGKILL', p, pid)
        os.killpg(os.getpgid(pid), signal.SIGKILL)
        (gone, alive) = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)
        if alive:
            for p in alive:
                log.error('Process %s (%s) could not be killed. Giving up.', p, p.pid)
