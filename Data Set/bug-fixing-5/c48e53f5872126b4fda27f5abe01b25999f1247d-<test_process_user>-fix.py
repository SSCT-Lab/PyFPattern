def test_process_user(self) -> None:
    user_id_mapper = IdMapper()
    harry_dict = self.username_to_user['harry']
    harry_dict['is_mirror_dummy'] = False
    realm_id = 3
    team_name = 'gryffindor'
    user = process_user(harry_dict, realm_id, team_name, user_id_mapper)
    self.assertEqual(user['avatar_source'], 'G')
    self.assertEqual(user['delivery_email'], 'harry@zulip.com')
    self.assertEqual(user['email'], 'harry@zulip.com')
    self.assertEqual(user['full_name'], 'Harry Potter')
    self.assertEqual(user['id'], 1)
    self.assertEqual(user['is_active'], True)
    self.assertEqual(user['is_realm_admin'], True)
    self.assertEqual(user['is_guest'], False)
    self.assertEqual(user['is_mirror_dummy'], False)
    self.assertEqual(user['realm'], 3)
    self.assertEqual(user['short_name'], 'harry')
    self.assertEqual(user['timezone'], 'UTC')
    harry_dict['teams'] = None
    user = process_user(harry_dict, realm_id, team_name, user_id_mapper)
    self.assertEqual(user['is_realm_admin'], False)
    team_name = 'slytherin'
    snape_dict = self.username_to_user['snape']
    snape_dict['is_mirror_dummy'] = True
    user = process_user(snape_dict, realm_id, team_name, user_id_mapper)
    self.assertEqual(user['avatar_source'], 'G')
    self.assertEqual(user['delivery_email'], 'snape@zulip.com')
    self.assertEqual(user['email'], 'snape@zulip.com')
    self.assertEqual(user['full_name'], 'Severus Snape')
    self.assertEqual(user['id'], 2)
    self.assertEqual(user['is_active'], False)
    self.assertEqual(user['is_realm_admin'], False)
    self.assertEqual(user['is_guest'], False)
    self.assertEqual(user['is_mirror_dummy'], True)
    self.assertEqual(user['realm'], 3)
    self.assertEqual(user['short_name'], 'snape')
    self.assertEqual(user['timezone'], 'UTC')