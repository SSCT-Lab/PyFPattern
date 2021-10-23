@override_settings(USE_THOUSAND_SEPARATOR=True, USE_L10N=True)
def test_non_localized_pk(self):
    'If USE_THOUSAND_SEPARATOR is set, make sure that the ids for\n        the objects selected for deletion are rendered without separators.\n        Refs #14895.\n        '
    s = ExternalSubscriber.objects.create(id=9999)
    action_data = {
        ACTION_CHECKBOX_NAME: [s.pk, self.s2.pk],
        'action': 'delete_selected',
        'index': 0,
    }
    response = self.client.post(reverse('admin:admin_views_subscriber_changelist'), action_data)
    self.assertTemplateUsed(response, 'admin/delete_selected_confirmation.html')
    self.assertContains(response, 'value="9999"')
    self.assertContains(response, ('value="%s"' % self.s2.pk))