def test_notify_sentry_app_and_plugin_with_same_slug(self):
    event = self.get_event()
    self.create_sentry_app(organization=event.organization, name='Notify', is_alertable=True)
    plugin = MagicMock()
    plugin.is_enabled.return_value = True
    plugin.should_notify.return_value = True
    rule = self.get_rule(data={
        'service': 'notify',
    })
    with patch('sentry.plugins.plugins.get') as get_plugin:
        get_plugin.return_value = plugin
        results = list(rule.after(event=event, state=self.get_state()))
    assert (len(results) == 2)
    assert (plugin.should_notify.call_count == 1)
    assert (results[0].callback is notify_sentry_app)
    assert (results[1].callback is plugin.rule_notify)