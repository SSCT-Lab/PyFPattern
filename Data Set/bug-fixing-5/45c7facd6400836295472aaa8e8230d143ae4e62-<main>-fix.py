def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(vpc_id=dict(required=True), state=dict(default='present', choices=['present', 'absent']), tags=dict(default=dict(), required=False, type='dict', aliases=['resource_tags'])))
    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)
    results = dict(changed=False)
    igw_manager = AnsibleEc2Igw(module=module, results=results)
    igw_manager.process()
    module.exit_json(**results)