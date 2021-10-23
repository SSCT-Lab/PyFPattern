def test_create_jks_fail_export_pkcs12(self):
    set_module_args(dict(certificate='cert-foo', private_key='private-foo', dest='/etc/security/keystore.jks', name='foo', password='changeit'))
    module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
    module.fail_json = Mock()
    with patch('os.remove', return_value=True):
        self.run_commands.side_effect = [(1, '', ''), (0, '', '')]
        create_jks(module, 'test', 'openssl', 'keytool', '/etc/security/keystore.jks', 'changeit')
        module.fail_json.assert_called_once_with(cmd="openssl pkcs12 -export -name 'test' -in '/tmp/foo.crt' -inkey '/tmp/foo.key' -out '/tmp/keystore.p12' -passout 'pass:changeit'", msg='', rc=1)