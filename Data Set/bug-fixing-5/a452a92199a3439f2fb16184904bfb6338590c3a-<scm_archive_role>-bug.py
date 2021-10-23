@staticmethod
def scm_archive_role(src, scm='git', name=None, version='HEAD', keep_scm_meta=False):

    def run_scm_cmd(cmd, tempdir):
        try:
            stdout = None
            stderr = None
            popen = Popen(cmd, cwd=tempdir, stdout=PIPE, stderr=PIPE)
            (stdout, stderr) = popen.communicate()
        except Exception as e:
            ran = ' '.join(cmd)
            display.debug(('ran %s:' % ran))
            display.debug(('\tstdout: ' + stdout))
            display.debug(('\tstderr: ' + stderr))
            raise AnsibleError(('when executing %s: %s' % (ran, to_native(e))))
        if (popen.returncode != 0):
            raise AnsibleError(('- command %s failed in directory %s (rc=%s)' % (' '.join(cmd), tempdir, popen.returncode)))
    if (scm not in ['hg', 'git']):
        raise AnsibleError(('- scm %s is not currently supported' % scm))
    try:
        scm_path = get_bin_path(scm)
    except (ValueError, OSError, IOError):
        raise AnsibleError(('could not find/use %s, it is required to continue with installing %s' % (scm, src)))
    tempdir = tempfile.mkdtemp(dir=C.DEFAULT_LOCAL_TMP)
    clone_cmd = [scm_path, 'clone', src, name]
    run_scm_cmd(clone_cmd, tempdir)
    if ((scm == 'git') and version):
        checkout_cmd = [scm_path, 'checkout', version]
        run_scm_cmd(checkout_cmd, os.path.join(tempdir, name))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tar', dir=C.DEFAULT_LOCAL_TMP)
    archive_cmd = None
    if keep_scm_meta:
        display.vvv(('tarring %s from %s to %s' % (name, tempdir, temp_file.name)))
        with tarfile.open(temp_file.name, 'w') as tar:
            tar.add(os.path.join(tempdir, name), arcname=name)
    elif (scm == 'hg'):
        archive_cmd = [scm_path, 'archive', '--prefix', ('%s/' % name)]
        if version:
            archive_cmd.extend(['-r', version])
        archive_cmd.append(temp_file.name)
    elif (scm == 'git'):
        archive_cmd = [scm_path, 'archive', ('--prefix=%s/' % name), ('--output=%s' % temp_file.name)]
        if version:
            archive_cmd.append(version)
        else:
            archive_cmd.append('HEAD')
    if (archive_cmd is not None):
        display.vvv(('archiving %s' % archive_cmd))
        run_scm_cmd(archive_cmd, os.path.join(tempdir, name))
    return temp_file.name