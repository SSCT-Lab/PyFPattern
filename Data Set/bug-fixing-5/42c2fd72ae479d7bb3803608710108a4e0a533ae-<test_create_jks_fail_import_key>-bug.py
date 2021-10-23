def test_create_jks_fail_import_key(self):
    set_module_args(dict(certificate='cert-foo', private_key='private-foo', dest='/etc/security/keystore.jks', name='foo', password='changeit'))
    module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
    module.fail_json = Mock()
    with patch('os.remove', return_value=True):
        self.run_commands.side_effect = [(0, '', ''), (1, '', '')]
        create_jks(module, 'test', 'openssl', 'keytool', '/etc/security/keystore.jks', 'changeit')
        module.fail_json.assert_called_once_with(cmd="keytool -importkeystore -destkeystore '/etc/security/keystore.jks' -srckeystore '/tmp/keystore.p12' -srcstoretype pkcs12 -alias 'test' -deststorepass 'changeit' -srcstorepass 'changeit' -noprompt", msg='', rc=1)