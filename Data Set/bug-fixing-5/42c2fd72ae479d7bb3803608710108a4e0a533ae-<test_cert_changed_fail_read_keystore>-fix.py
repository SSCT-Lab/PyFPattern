def test_cert_changed_fail_read_keystore(self):
    set_module_args(dict(certificate='cert-foo', private_key='private-foo', dest='/path/to/keystore.jks', name='foo', password='changeit'))
    module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
    module.fail_json = Mock(return_value=True)
    with patch('os.remove', return_value=True):
        self.run_commands.side_effect = [(0, 'foo: wxyz:9876:stuv', ''), (1, '', 'Oops')]
        cert_changed(module, 'openssl', 'keytool', '/path/to/keystore.jks', 'changeit', 'foo')
        module.fail_json.assert_called_with(cmd="keytool -list -alias 'foo' -keystore '/path/to/keystore.jks' -storepass 'changeit'", msg='', err='Oops', rc=1)