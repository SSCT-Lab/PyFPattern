def format_shippable_group_alias(self, name, fallback=''):
    '\n        :type name: str\n        :type fallback: str\n        :rtype: str\n        '
    group_numbers = self.shippable_test_groups.get(name, None)
    if group_numbers:
        if (min(group_numbers) != 1):
            display.warning(('Min test group "%s" in shippable.yml is %d instead of 1.' % (name, min(group_numbers))), unique=True)
        if (max(group_numbers) != len(group_numbers)):
            display.warning(('Max test group "%s" in shippable.yml is %d instead of %d.' % (name, max(group_numbers), len(group_numbers))), unique=True)
        if (len(group_numbers) > 1):
            alias = ('shippable/%s/group[%d-%d]/' % (name, min(group_numbers), max(group_numbers)))
        else:
            alias = ('shippable/%s/group%d/' % (name, min(group_numbers)))
    elif fallback:
        alias = ('shippable/%s/group%d/' % (fallback, 1))
    else:
        raise Exception(('cannot find test group "%s" in shippable.yml' % name))
    return alias