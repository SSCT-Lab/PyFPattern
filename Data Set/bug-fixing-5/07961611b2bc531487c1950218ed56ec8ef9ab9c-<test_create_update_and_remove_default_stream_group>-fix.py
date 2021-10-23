def test_create_update_and_remove_default_stream_group(self) -> None:
    realm = get_realm('zulip')
    default_stream_groups = get_default_stream_groups(realm)
    self.assert_length(default_stream_groups, 0)
    streams = []
    for stream_name in ['stream1', 'stream2', 'stream3']:
        (stream, _) = create_stream_if_needed(realm, stream_name)
        streams.append(stream)

    def get_streams(group: DefaultStreamGroup) -> List[Stream]:
        return list(group.streams.all().order_by('name'))
    group_name = 'group1'
    description = 'This is group1'
    do_create_default_stream_group(realm, group_name, description, streams)
    default_stream_groups = get_default_stream_groups(realm)
    self.assert_length(default_stream_groups, 1)
    self.assertEqual(default_stream_groups[0].name, group_name)
    self.assertEqual(default_stream_groups[0].description, description)
    self.assertEqual(get_streams(default_stream_groups[0]), streams)
    group = lookup_default_stream_groups(['group1'], realm)[0]
    new_stream_names = ['stream4', 'stream5']
    new_streams = []
    for new_stream_name in new_stream_names:
        (new_stream, _) = create_stream_if_needed(realm, new_stream_name)
        new_streams.append(new_stream)
        streams.append(new_stream)
    do_add_streams_to_default_stream_group(realm, group, new_streams)
    default_stream_groups = get_default_stream_groups(realm)
    self.assert_length(default_stream_groups, 1)
    self.assertEqual(default_stream_groups[0].name, group_name)
    self.assertEqual(get_streams(default_stream_groups[0]), streams)
    do_remove_streams_from_default_stream_group(realm, group, new_streams)
    remaining_streams = streams[0:3]
    default_stream_groups = get_default_stream_groups(realm)
    self.assert_length(default_stream_groups, 1)
    self.assertEqual(default_stream_groups[0].name, group_name)
    self.assertEqual(get_streams(default_stream_groups[0]), remaining_streams)
    new_description = 'group1 new description'
    do_change_default_stream_group_description(realm, group, new_description)
    default_stream_groups = get_default_stream_groups(realm)
    self.assertEqual(default_stream_groups[0].description, new_description)
    self.assert_length(default_stream_groups, 1)
    new_group_name = 'new group1'
    do_change_default_stream_group_name(realm, group, new_group_name)
    default_stream_groups = get_default_stream_groups(realm)
    self.assert_length(default_stream_groups, 1)
    self.assertEqual(default_stream_groups[0].name, new_group_name)
    self.assertEqual(get_streams(default_stream_groups[0]), remaining_streams)
    do_remove_default_stream_group(realm, group)
    default_stream_groups = get_default_stream_groups(realm)
    self.assert_length(default_stream_groups, 0)
    do_add_default_stream(remaining_streams[0])
    with self.assertRaisesRegex(JsonableError, "'stream1' is a default stream and cannot be added to 'new group1'"):
        do_create_default_stream_group(realm, new_group_name, 'This is group1', remaining_streams)