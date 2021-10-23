

def test_realm_filter_events(self) -> None:
    schema_checker = self.check_events_dict([('type', equals('realm_filters')), ('realm_filters', check_list(None))])
    events = self.do_test((lambda : do_add_realm_filter(self.user_profile.realm, '#(?P<id>[123])', 'https://realm.com/my_realm_filter/%(id)s')))
    error = schema_checker('events[0]', events[0])
    self.assert_on_error(error)
    self.do_test((lambda : do_remove_realm_filter(self.user_profile.realm, '#(?P<id>[123])')))
    error = schema_checker('events[0]', events[0])
    self.assert_on_error(error)
