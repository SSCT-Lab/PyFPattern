def create_script(command):
    'Write out a script onto a target.\n\n    This method should be backward compatible with Python 2.4+ when executing\n    from within the container.\n\n    :param command: command to run, this can be a script and can use spacing\n                    with newlines as separation.\n    :type command: ``str``\n    '
    (fd, script_file) = tempfile.mkstemp(prefix='lxc-attach-script')
    f = os.fdopen(fd, 'wb')
    try:
        f.write(to_bytes((ATTACH_TEMPLATE % {
            'container_command': command,
        }), errors='surrogate_or_strict'))
        f.flush()
    finally:
        f.close()
    os.chmod(script_file, int('0700', 8))
    stdout_file = os.fdopen(tempfile.mkstemp(prefix='lxc-attach-script-log')[0], 'ab')
    stderr_file = os.fdopen(tempfile.mkstemp(prefix='lxc-attach-script-err')[0], 'ab')
    try:
        subprocess.Popen([script_file], stdout=stdout_file, stderr=stderr_file).communicate()
    finally:
        stderr_file.close()
        stdout_file.close()
        os.remove(script_file)