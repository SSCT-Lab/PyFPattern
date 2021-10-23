def test_object_update_fk(self):
    test_gmbh = Company.objects.get(pk=self.gmbh.pk)
    msg = 'F(ceo)": "Company.point_of_contact" must be a "Employee" instance.'
    with self.assertRaisesMessage(ValueError, msg):
        test_gmbh.point_of_contact = F('ceo')
    test_gmbh.point_of_contact = self.gmbh.ceo
    test_gmbh.save()
    test_gmbh.name = F('ceo__lastname')
    msg = 'Joined field references are not permitted in this query'
    with self.assertRaisesMessage(FieldError, msg):
        test_gmbh.save()