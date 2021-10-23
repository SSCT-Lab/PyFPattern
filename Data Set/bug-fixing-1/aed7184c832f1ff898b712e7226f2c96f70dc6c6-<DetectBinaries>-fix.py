

def DetectBinaries(which=None, use_cache=True, preferred={
    
}, skip=None, _raise=None):
    import mailpile.util
    import mailpile.safe_popen
    import traceback
    global BINARIES
    if (which and use_cache):
        if (which in BINARIES):
            return BINARIES[which]
        env_bin = os.getenv(('MAILPILE_%s' % which.upper()), '')
        if env_bin:
            BINARIES[which] = env_bin
            return env_bin
    if (skip is None):
        skip = os.getenv('MAILPILE_IGNORE_BINARIES', '').split()

    def _run_bintest(bt):
        p = mailpile.safe_popen.Popen(bt, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.communicate()
    for (binary, binary_test) in BINARIES_WANTED.iteritems():
        if (binary in skip):
            continue
        if ((which is None) or (binary == which)):
            if preferred.get(binary):
                binary_test = copy.copy(binary_test)
                binary_test[0] = preferred[binary]
            else:
                env_bin = os.getenv(('MAILPILE_%s' % binary.upper()), '')
                if env_bin:
                    BINARIES[binary] = env_bin
                    continue
            try:
                mailpile.util.RunTimed(5.0, _run_bintest, binary_test)
                BINARIES[binary] = binary_test[0]
                if ((not os.path.dirname(BINARIES[binary])) and (not sys.platform.startswith('win'))):
                    try:
                        path = subprocess.check_output(['which', BINARIES[binary]])
                        if path:
                            BINARIES[binary] = path.strip()
                    except (OSError, subprocess.CalledProcessError):
                        pass
            except (OSError, subprocess.CalledProcessError, mailpile.util.TimedOut):
                if (binary in BINARIES):
                    del BINARIES[binary]
    if which:
        if (_raise not in (None, False)):
            if (not BINARIES.get(which)):
                raise _raise(('%s not found' % which))
        return BINARIES.get(which)
    elif (_raise not in (None, False)):
        for (binary, binary_test) in BINARIES_WANTED.iteritems():
            if (binary in skip):
                continue
            if (not BINARIES.get(binary)):
                raise _raise(('%s not found' % binary))
    return BINARIES
