

def test_end_to_end_with_actions_dot_py(self) -> None:
    user1 = do_create_user('email1', 'password', self.default_realm, 'full_name', 'short_name')
    user2 = do_create_user('email2', 'password', self.default_realm, 'full_name', 'short_name')
    user3 = do_create_user('email3', 'password', self.default_realm, 'full_name', 'short_name')
    user4 = do_create_user('email4', 'password', self.default_realm, 'full_name', 'short_name')
    do_deactivate_user(user2)
    do_activate_user(user3)
    do_reactivate_user(user4)
    end_time = (floor_to_day(timezone_now()) + self.DAY)
    do_fill_count_stat_at_hour(self.stat, end_time)
    for user in [user1, user3, user4]:
        self.assertTrue(UserCount.objects.filter(user=user, property=self.current_property, subgroup='false', end_time=end_time, value=1).exists())
    self.assertFalse(UserCount.objects.filter(user=user2).exists())
