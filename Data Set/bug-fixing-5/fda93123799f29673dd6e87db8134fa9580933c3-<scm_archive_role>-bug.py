@staticmethod
def scm_archive_role(src, scm='git', name=None, version='HEAD', keep_scm_meta=False):
    if (scm not in ['hg', 'git']):
        raise AnsibleError(('- scm %s is not currently supported' % scm))
    tempdir = tempfile.mkdtemp()
    clone_cmd = [scm, 'clone', src, name]
    with open('/dev/null', 'w') as devnull:
        try:
            popen = subprocess.Popen(clone_cmd, cwd=tempdir, stdout=devnull, stderr=devnull)
        except:
            raise AnsibleError(('error executing: %s' % ' '.join(clone_cmd)))
        rc = popen.wait()
    if (rc != 0):
        raise AnsibleError(('- command %s failed in directory %s (rc=%s)' % (' '.join(clone_cmd), tempdir, rc)))
    if ((scm == 'git') and version):
        checkout_cmd = [scm, 'checkout', version]
        with open('/dev/null', 'w') as devnull:
            try:
                popen = subprocess.Popen(checkout_cmd, cwd=os.path.join(tempdir, name), stdout=devnull, stderr=devnull)
            except (IOError, OSError):
                raise AnsibleError(('error executing: %s' % ' '.join(checkout_cmd)))
            rc = popen.wait()
        if (rc != 0):
            raise AnsibleError(('- command %s failed in directory %s (rc=%s)' % (' '.join(checkout_cmd), tempdir, rc)))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.tar')
    archive_cmd = None
    if keep_scm_meta:
        display.vvv(('tarring %s from %s to %s' % (name, tempdir, temp_file.name)))
        with tarfile.open(temp_file.name, 'w') as tar:
            tar.add(os.path.join(tempdir, name), arcname=name)
    elif (scm == 'hg'):
        archive_cmd = ['hg', 'archive', '--prefix', ('%s/' % name)]
        if version:
            archive_cmd.extend(['-r', version])
        archive_cmd.append(temp_file.name)
    elif (scm == 'git'):
        archive_cmd = ['git', 'archive', ('--prefix=%s/' % name), ('--output=%s' % temp_file.name)]
        if version:
            archive_cmd.append(version)
        else:
            archive_cmd.append('HEAD')
    if (archive_cmd is not None):
        display.vvv(('archiving %s' % archive_cmd))
        with open('/dev/null', 'w') as devnull:
            popen = subprocess.Popen(archive_cmd, cwd=os.path.join(tempdir, name), stderr=devnull, stdout=devnull)
            rc = popen.wait()
        if (rc != 0):
            raise AnsibleError(('- command %s failed in directory %s (rc=%s)' % (' '.join(archive_cmd), tempdir, rc)))
    shutil.rmtree(tempdir, ignore_errors=True)
    return temp_file.name