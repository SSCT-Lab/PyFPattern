def make_external_conversion_command(cmd):

    def convert(old, new):
        cmdline = cmd(old, new)
        pipe = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = pipe.communicate()
        errcode = pipe.wait()
        if ((not os.path.exists(new)) or errcode):
            msg = ('Conversion command failed:\n%s\n' % ' '.join(cmdline))
            if stdout:
                msg += ('Standard output:\n%s\n' % stdout)
            if stderr:
                msg += ('Standard error:\n%s\n' % stderr)
            raise IOError(msg)
    return convert