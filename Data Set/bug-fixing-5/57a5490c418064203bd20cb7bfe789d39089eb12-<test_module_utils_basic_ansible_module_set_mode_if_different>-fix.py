def test_module_utils_basic_ansible_module_set_mode_if_different(self):
    with patch('os.lstat') as m:
        with patch('os.lchmod', return_value=None, create=True) as m_os:
            m.side_effect = [self.mock_stat1, self.mock_stat2, self.mock_stat2]
            self.am._symbolic_mode_to_octal = MagicMock(side_effect=Exception)
            with pytest.raises(SystemExit):
                self.am.set_mode_if_different('/path/to/file', 'o+w,g+w,a-r', False)
    original_hasattr = hasattr

    def _hasattr(obj, name):
        if ((obj == os) and (name == 'lchmod')):
            return False
        return original_hasattr(obj, name)
    with patch('os.lstat', side_effect=[self.mock_stat1, self.mock_stat2]):
        with patch.object(builtins, 'hasattr', side_effect=_hasattr):
            with patch('os.path.islink', return_value=False):
                with patch('os.chmod', return_value=None) as m_chmod:
                    self.assertEqual(self.am.set_mode_if_different('/path/to/file/no_lchmod', 432, False), True)
    with patch('os.lstat', side_effect=[self.mock_stat1, self.mock_stat2]):
        with patch.object(builtins, 'hasattr', side_effect=_hasattr):
            with patch('os.path.islink', return_value=True):
                with patch('os.chmod', return_value=None) as m_chmod:
                    with patch('os.stat', return_value=self.mock_stat2):
                        self.assertEqual(self.am.set_mode_if_different('/path/to/file', 432, False), True)