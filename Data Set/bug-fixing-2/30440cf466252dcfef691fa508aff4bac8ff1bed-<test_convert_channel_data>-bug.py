

def test_convert_channel_data(self) -> None:
    user_handler = UserHandler()
    subscriber_handler = SubscriberHandler()
    stream_id_mapper = IdMapper()
    user_id_mapper = IdMapper()
    team_name = 'gryffindor'
    convert_user_data(user_handler=user_handler, user_id_mapper=user_id_mapper, user_data_map=self.username_to_user, realm_id=3, team_name=team_name)
    zerver_stream = convert_channel_data(channel_data=self.mattermost_data['channel'], user_data_map=self.username_to_user, subscriber_handler=subscriber_handler, stream_id_mapper=stream_id_mapper, user_id_mapper=user_id_mapper, realm_id=3, team_name=team_name)
    self.assertEqual(len(zerver_stream), 3)
    self.assertEqual(zerver_stream[0]['name'], 'Gryffindor common room')
    self.assertEqual(zerver_stream[0]['invite_only'], False)
    self.assertEqual(zerver_stream[0]['description'], 'A place for talking about Gryffindor common room')
    self.assertEqual(zerver_stream[0]['rendered_description'], '')
    self.assertEqual(zerver_stream[0]['realm'], 3)
    self.assertEqual(zerver_stream[1]['name'], 'Gryffindor quidditch team')
    self.assertEqual(zerver_stream[1]['invite_only'], False)
    self.assertEqual(zerver_stream[1]['description'], 'A place for talking about Gryffindor quidditch team')
    self.assertEqual(zerver_stream[1]['rendered_description'], '')
    self.assertEqual(zerver_stream[1]['realm'], 3)
    self.assertEqual(zerver_stream[2]['name'], 'Dumbledores army')
    self.assertEqual(zerver_stream[2]['invite_only'], True)
    self.assertEqual(zerver_stream[2]['description'], 'A place for talking about Dumbledores army')
    self.assertEqual(zerver_stream[2]['rendered_description'], '')
    self.assertEqual(zerver_stream[2]['realm'], 3)
    self.assertTrue(stream_id_mapper.has('gryffindor-common-room'))
    self.assertTrue(stream_id_mapper.has('gryffindor-quidditch-team'))
    self.assertTrue(stream_id_mapper.has('dumbledores-army'))
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('gryffindor-common-room')), {1, 2})
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('gryffindor-quidditch-team')), {1, 2})
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('dumbledores-army')), {1, 2})
    self.username_to_user['ron'].update({
        'teams': None,
    })
    zerver_stream = convert_channel_data(channel_data=self.mattermost_data['channel'], user_data_map=self.username_to_user, subscriber_handler=subscriber_handler, stream_id_mapper=stream_id_mapper, user_id_mapper=user_id_mapper, realm_id=3, team_name=team_name)
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('gryffindor-common-room')), {2})
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('gryffindor-quidditch-team')), {2})
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('dumbledores-army')), {2})
    team_name = 'slytherin'
    zerver_stream = convert_channel_data(channel_data=self.mattermost_data['channel'], user_data_map=self.username_to_user, subscriber_handler=subscriber_handler, stream_id_mapper=stream_id_mapper, user_id_mapper=user_id_mapper, realm_id=4, team_name=team_name)
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('slytherin-common-room')), {3, 4, 5})
    self.assertEqual(subscriber_handler.get_users(stream_id_mapper.get('slytherin-quidditch-team')), {3, 4})
