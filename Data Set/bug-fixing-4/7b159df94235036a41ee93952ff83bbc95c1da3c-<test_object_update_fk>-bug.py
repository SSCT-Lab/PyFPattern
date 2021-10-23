def test_object_update_fk(self):

    def test():
        self.gmbh.point_of_contact = F('ceo')
    msg = 'F(ceo)": "Company.point_of_contact" must be a "Employee" instance.'
    with self.assertRaisesMessage(ValueError, msg):
        test()
    self.gmbh.point_of_contact = self.gmbh.ceo
    self.gmbh.save()
    self.gmbh.name = F('ceo__last_name')
    msg = 'Joined field references are not permitted in this query'
    with self.assertRaisesMessage(FieldError, msg):
        self.gmbh.save()