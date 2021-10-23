def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str', required=True), resource_id=dict(aliases=['droplet_id'], type='int'), resource_type=dict(choices=['droplet'], default='droplet'), state=dict(choices=['present', 'absent'], default='present'), api_token=dict(aliases=['API_TOKEN'], no_log=True)))
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())