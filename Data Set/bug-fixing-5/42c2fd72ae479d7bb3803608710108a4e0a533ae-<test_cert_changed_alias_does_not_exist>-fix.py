def test_cert_changed_alias_does_not_exist(self):
    set_module_args(dict(certificate='cert-foo', private_key='private-foo', dest='/path/to/keystore.jks', name='foo', password='changeit'))
    module = AnsibleModule(argument_spec=self.spec.argument_spec, supports_check_mode=self.spec.supports_check_mode)
    with patch('os.remove', return_value=True):
        self.run_commands.side_effect = [(0, 'foo=abcd:1234:efgh', ''), (1, 'keytool error: java.lang.Exception: Alias <foo> does not exist', '')]
        result = cert_changed(module, 'openssl', 'keytool', '/path/to/keystore.jks', 'changeit', 'foo')
        self.assertTrue(result, 'Certificate does not exist')