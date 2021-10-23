

def main():
    module = AnsibleModule(argument_spec=dict(group_id=dict(required=True), artifact_id=dict(required=True), version=dict(default='latest'), classifier=dict(default=''), extension=dict(default='jar'), repository_url=dict(default=None), username=dict(default=None, aliases=['aws_secret_key']), password=dict(default=None, no_log=True, aliases=['aws_secret_access_key']), state=dict(default='present', choices=['present', 'absent']), timeout=dict(default=10, type='int'), dest=dict(type='path', required=True), validate_certs=dict(required=False, default=True, type='bool'), keep_name=dict(required=False, default=False, type='bool'), verify_checksum=dict(required=False, default='download', choices=['never', 'download', 'change', 'always'])), add_file_common_args=True)
    if (not HAS_LXML_ETREE):
        module.fail_json(msg='module requires the lxml python library installed on the managed machine')
    repository_url = module.params['repository_url']
    if (not repository_url):
        repository_url = 'http://repo1.maven.org/maven2'
    try:
        parsed_url = urlparse(repository_url)
    except AttributeError as e:
        module.fail_json(msg=('url parsing went wrong %s' % e))
    local = (parsed_url.scheme == 'file')
    if ((parsed_url.scheme == 's3') and (not HAS_BOTO)):
        module.fail_json(msg='boto3 required for this module, when using s3:// repository URLs')
    group_id = module.params['group_id']
    artifact_id = module.params['artifact_id']
    version = module.params['version']
    classifier = module.params['classifier']
    extension = module.params['extension']
    state = module.params['state']
    dest = module.params['dest']
    b_dest = to_bytes(dest, errors='surrogate_or_strict')
    keep_name = module.params['keep_name']
    verify_checksum = module.params['verify_checksum']
    verify_download = (verify_checksum in ['download', 'always'])
    verify_change = (verify_checksum in ['change', 'always'])
    downloader = MavenDownloader(module, repository_url, local)
    try:
        artifact = Artifact(group_id, artifact_id, version, classifier, extension)
    except ValueError as e:
        module.fail_json(msg=e.args[0])
    changed = False
    prev_state = 'absent'
    if dest.endswith(os.sep):
        b_dest = to_bytes(dest, errors='surrogate_or_strict')
        if (not os.path.exists(b_dest)):
            (pre_existing_dir, new_directory_list) = split_pre_existing_dir(dest)
            os.makedirs(b_dest)
            directory_args = module.load_file_common_arguments(module.params)
            directory_mode = module.params['directory_mode']
            if (directory_mode is not None):
                directory_args['mode'] = directory_mode
            else:
                directory_args['mode'] = None
            changed = adjust_recursive_directory_permissions(pre_existing_dir, new_directory_list, module, directory_args, changed)
    if os.path.isdir(b_dest):
        version_part = version
        if (keep_name and (version == 'latest')):
            version_part = downloader.find_latest_version_available(artifact)
        if classifier:
            dest = posixpath.join(dest, ('%s-%s-%s.%s' % (artifact_id, version_part, classifier, extension)))
        else:
            dest = posixpath.join(dest, ('%s-%s.%s' % (artifact_id, version_part, extension)))
        b_dest = to_bytes(dest, errors='surrogate_or_strict')
    if (os.path.lexists(b_dest) and ((not verify_change) or (not downloader.is_invalid_md5(dest, downloader.find_uri_for_artifact(artifact))))):
        prev_state = 'present'
    if (prev_state == 'absent'):
        try:
            download_error = downloader.download(module.tmpdir, artifact, verify_download, b_dest)
            if (download_error is None):
                changed = True
            else:
                module.fail_json(msg=('Cannot retrieve the artifact to destination: ' + download_error))
        except ValueError as e:
            module.fail_json(msg=e.args[0])
    module.params['dest'] = dest
    file_args = module.load_file_common_arguments(module.params)
    changed = module.set_fs_attributes_if_different(file_args, changed)
    if changed:
        module.exit_json(state=state, dest=dest, group_id=group_id, artifact_id=artifact_id, version=version, classifier=classifier, extension=extension, repository_url=repository_url, changed=changed)
    else:
        module.exit_json(state=state, dest=dest, changed=changed)
