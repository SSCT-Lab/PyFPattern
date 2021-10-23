def verify(filename):
    'Verify the file through some sort of verification tool.'
    if (not os.path.exists(filename)):
        raise IOError(("'%s' does not exist" % filename))
    (base, extension) = filename.rsplit('.', 1)
    verifier = verifiers.get(extension, None)
    if (verifier is not None):
        cmd = verifier(filename)
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = pipe.communicate()
        errcode = pipe.wait()
        if (errcode != 0):
            msg = ('File verification command failed:\n%s\n' % ' '.join(cmd))
            if stdout:
                msg += ('Standard output:\n%s\n' % stdout)
            if stderr:
                msg += ('Standard error:\n%s\n' % stderr)
            raise IOError(msg)