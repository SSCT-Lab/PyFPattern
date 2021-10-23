def test_module_utils_basic_ansible_module_user_and_group(self):
    from ansible.module_utils import basic
    basic._ANSIBLE_ARGS = None
    am = basic.AnsibleModule(argument_spec=dict())
    mock_stat = MagicMock()
    mock_stat.st_uid = 0
    mock_stat.st_gid = 0
    with patch('os.lstat', return_value=mock_stat):
        self.assertEqual(am.user_and_group('/path/to/file'), (0, 0))