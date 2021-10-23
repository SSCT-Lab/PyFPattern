def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(names={
        'default': [],
        'type': 'list',
    }))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    try:
        (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
        if (not region):
            module.fail_json(msg='region must be specified')
        names = module.params['names']
        elb_information = ElbInformation(module, names, region, **aws_connect_params)
        ec2_facts_result = dict(changed=False, elbs=elb_information.list_elbs())
    except BotoServerError as err:
        self.module.fail_json(msg='{0}: {1}'.format(err.error_code, err.error_message), exception=traceback.format_exc())
    module.exit_json(**ec2_facts_result)