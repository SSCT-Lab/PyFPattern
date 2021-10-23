

def test_module_utils_basic_ansible_module__symbolic_mode_to_octal(self):
    from ansible.module_utils import basic
    basic._ANSIBLE_ARGS = None
    am = basic.AnsibleModule(argument_spec=dict())
    mock_stat = MagicMock()
    mock_stat.st_mode = 16384
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'a+rwx'), 511)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'u+rwx,g+rwx,o+rwx'), 511)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'o+rwx'), 7)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'g+rwx'), 56)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'u+rwx'), 448)
    mock_stat.st_mode = 16895
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'a-rwx'), 0)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'u-rwx,g-rwx,o-rwx'), 0)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'o-rwx'), 504)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'g-rwx'), 455)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'u-rwx'), 63)
    mock_stat.st_mode = 16384
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'a=rwx'), 511)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'u=rwx,g=rwx,o=rwx'), 511)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'o=rwx'), 7)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'g=rwx'), 56)
    self.assertEqual(am._symbolic_mode_to_octal(mock_stat, 'u=rwx'), 448)
    mock_stat.st_mode = 16384
    self.assertRaises(ValueError, am._symbolic_mode_to_octal, mock_stat, 'a=foo')
