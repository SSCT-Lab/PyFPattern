def test_root_non_number(self):
    with pytest.raises(AnsibleFilterError, match="root\\(\\) can only be used on numbers: (could not convert string to float: a|could not convert string to float: 'a')"):
        ms.inversepower(10, 'a')
    with pytest.raises(AnsibleFilterError, match='root\\(\\) can only be used on numbers: (a float is required|must be real number, not str)'):
        ms.inversepower('a', 10)