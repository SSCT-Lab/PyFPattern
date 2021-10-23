def test_warn_region_not_specified():
    set_module_args({
        'name': 'lambda_name',
        'state': 'present',
        'zip_file': 'test/units/modules/cloud/amazon/fixtures/thezip.zip',
        'runtime': 'python2.7',
        'role': 'arn:aws:iam::987654321012:role/lambda_basic_execution',
        'handler': 'lambda_python.my_handler',
    })

    class AnsibleFailJson(Exception):
        pass

    def fail_json(*args, **kwargs):
        kwargs['failed'] = True
        raise AnsibleFailJson(kwargs)

    def call_module():
        with patch.object(basic.AnsibleModule, 'fail_json', fail_json):
            try:
                lda.main()
            except AnsibleFailJson as e:
                result = e.args[0]
                assert ('region must be specified' in result['msg'])
    call_module()