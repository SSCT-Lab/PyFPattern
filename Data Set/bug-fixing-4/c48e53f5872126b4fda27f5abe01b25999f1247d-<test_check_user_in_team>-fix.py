def test_check_user_in_team(self) -> None:
    harry = self.username_to_user['harry']
    self.assertTrue(check_user_in_team(harry, 'gryffindor'))
    self.assertFalse(check_user_in_team(harry, 'slytherin'))
    snape = self.username_to_user['snape']
    self.assertFalse(check_user_in_team(snape, 'gryffindor'))
    self.assertTrue(check_user_in_team(snape, 'slytherin'))
    snape.update({
        'teams': None,
    })
    self.assertFalse(check_user_in_team(snape, 'slytherin'))