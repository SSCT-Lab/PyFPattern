def test_cert_changed_fail_read_cert(self):
    set_module_args(dict(certificate='cert-foo', private_key='private-foo', dest='/path/to/keystore.jks', name='foo', password='changeit'))
    module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
    module.fail_json = Mock()
    with patch('os.remove', return_value=True):
        self.run_commands.side_effect = [(1, '', 'Oops'), (0, 'foo: wxyz:9876:stuv', '')]
        cert_changed(module, 'openssl', 'keytool', '/path/to/keystore.jks', 'changeit', 'foo')
        module.fail_json.assert_called_once_with(cmd='openssl x509 -noout -in /tmp/foo.crt -fingerprint -sha1', msg='', err='Oops', rc=1)