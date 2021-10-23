def main():
    argument_spec = dict(archive_path=dict(type='path'), container_limits=dict(type='dict'), dockerfile=dict(type='str'), force=dict(type='bool', default=False), http_timeout=dict(type='int'), load_path=dict(type='path'), name=dict(type='str', required=True), nocache=dict(type='str', default=False), path=dict(type='path', aliases=['build_path']), pull=dict(type='bool', default=True), push=dict(type='bool', default=False), repository=dict(type='str'), rm=dict(type='bool', default=True), state=dict(type='str', choices=['absent', 'present', 'build'], default='present'), tag=dict(type='str', default='latest'), use_tls=dict(type='str', default='no', choices=['no', 'encrypt', 'verify']), buildargs=dict(type='dict', default=None))
    client = AnsibleDockerClient(argument_spec=argument_spec, supports_check_mode=True)
    results = dict(changed=False, actions=[], image={
        
    })
    ImageManager(client, results)
    client.module.exit_json(**results)