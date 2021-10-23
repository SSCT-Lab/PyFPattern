def test_create_jks_success(self):
    set_module_args(dict(certificate='cert-foo', private_key='private-foo', dest='/etc/security/keystore.jks', name='foo', password='changeit'))
    module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
    module.exit_json = Mock()
    with patch('os.remove', return_value=True):
        self.run_commands.side_effect = (lambda args, kwargs: (0, '', ''))
        create_jks(module, 'test', 'openssl', 'keytool', '/etc/security/keystore.jks', 'changeit')
        module.exit_json.assert_called_once_with(changed=True, cmd="keytool -importkeystore -destkeystore '/etc/security/keystore.jks' -srckeystore '/tmp/keystore.p12' -srcstoretype pkcs12 -alias 'test' -deststorepass 'changeit' -srcstorepass 'changeit' -noprompt", msg='', rc=0, stdout_lines='')