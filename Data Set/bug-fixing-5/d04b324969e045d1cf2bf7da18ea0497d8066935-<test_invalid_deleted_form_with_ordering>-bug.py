def test_invalid_deleted_form_with_ordering(self):

    class Person(Form):
        name = CharField()
    PeopleForm = formset_factory(form=Person, can_delete=True, can_order=True)
    p = PeopleForm({
        'form-0-name': '',
        'form-0-DELETE': 'on',
        'form-TOTAL_FORMS': 1,
        'form-INITIAL_FORMS': 1,
        'form-MIN_NUM_FORMS': 0,
        'form-MAX_NUM_FORMS': 1,
    })
    self.assertTrue(p.is_valid())
    self.assertEqual(p.ordered_forms, [])