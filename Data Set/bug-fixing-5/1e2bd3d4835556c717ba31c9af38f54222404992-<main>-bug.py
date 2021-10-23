def main():
    module = AnsibleModule(argument_spec=dict(group_id=dict(default=None), artifact_id=dict(default=None), version=dict(default='latest'), classifier=dict(default=None), extension=dict(default='jar'), repository_url=dict(default=None), username=dict(default=None, aliases=['aws_secret_key']), password=dict(default=None, no_log=True, aliases=['aws_secret_access_key']), state=dict(default='present', choices=['present', 'absent']), timeout=dict(default=10, type='int'), dest=dict(type='path', default=None), validate_certs=dict(required=False, default=True, type='bool')))
    try:
        parsed_url = urlparse(module.params['repository_url'])
    except AttributeError as e:
        module.fail_json(msg=('url parsing went wrong %s' % e))
    if ((parsed_url.scheme == 's3') and (not HAS_BOTO)):
        module.fail_json(msg='boto3 required for this module, when using s3:// repository URLs')
    group_id = module.params['group_id']
    artifact_id = module.params['artifact_id']
    version = module.params['version']
    classifier = module.params['classifier']
    extension = module.params['extension']
    repository_url = module.params['repository_url']
    repository_username = module.params['username']
    repository_password = module.params['password']
    state = module.params['state']
    dest = module.params['dest']
    if (not repository_url):
        repository_url = 'http://repo1.maven.org/maven2'
    downloader = MavenDownloader(module, repository_url)
    try:
        artifact = Artifact(group_id, artifact_id, version, classifier, extension)
    except ValueError as e:
        module.fail_json(msg=e.args[0])
    prev_state = 'absent'
    if os.path.isdir(dest):
        dest = posixpath.join(dest, ((((artifact_id + '-') + version) + '.') + extension))
    if (os.path.lexists(dest) and downloader.verify_md5(dest, (downloader.find_uri_for_artifact(artifact) + '.md5'))):
        prev_state = 'present'
    else:
        path = os.path.dirname(dest)
        if (not os.path.exists(path)):
            os.makedirs(path)
    if (prev_state == 'present'):
        module.exit_json(dest=dest, state=state, changed=False)
    try:
        if downloader.download(artifact, dest):
            module.exit_json(state=state, dest=dest, group_id=group_id, artifact_id=artifact_id, version=version, classifier=classifier, extension=extension, repository_url=repository_url, changed=True)
        else:
            module.fail_json(msg='Unable to download the artifact')
    except ValueError as e:
        module.fail_json(msg=e.args[0])