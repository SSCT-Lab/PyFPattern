

def _is_package_installed(module, name, easy_install, executable_arguments):
    executable_arguments = (executable_arguments + ['--dry-run'])
    cmd = ('%s %s %s' % (easy_install, ' '.join(executable_arguments), name))
    (rc, status_stdout, status_stderr) = module.run_command(cmd)
    if rc:
        module.fail_json(msg=status_stderr)
    return (not (('Reading' in status_stdout) or ('Downloading' in status_stdout)))
