def test_archiving_messages_with_attachment(self) -> None:
    self._create_attachments()
    body1 = 'Some files here ...[zulip.txt](\n            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/zulip.txt)\n            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/temp_file.py ....\n            Some more.... http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/abc.py\n        '
    body2 = 'Some files here\n            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/zulip.txt ...\n            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/hello.txt ....\n            http://localhost:9991/user_uploads/1/31/4CBjtTLYZhk66pZrF8hnYGwc/new.py ....\n        '
    msg_ids = []
    msg_ids.append(self.send_personal_message(self.sender, self.recipient, body1))
    msg_ids.append(self.send_personal_message(self.sender, self.recipient, body2))
    attachment_id_to_message_ids = {
        
    }
    attachments = Attachment.objects.filter(messages__id__in=msg_ids)
    for attachment in attachments:
        attachment_id_to_message_ids[attachment.id] = {message.id for message in attachment.messages.all()}
    (user_msgs_ids_before, all_msgs_ids_before) = self._check_messages_before_archiving(msg_ids)
    attachments_ids_before = list(attachments.order_by('id').values_list('id', flat=True))
    self.assertEqual(ArchivedAttachment.objects.count(), 0)
    move_messages_to_archive(message_ids=msg_ids)
    self._check_messages_after_archiving(msg_ids, user_msgs_ids_before, all_msgs_ids_before)
    self.assertEqual(Attachment.objects.count(), 0)
    archived_attachments = ArchivedAttachment.objects.filter(messages__id__in=msg_ids)
    arc_attachments_ids_after = list(archived_attachments.order_by('id').values_list('id', flat=True))
    self.assertEqual(attachments_ids_before, arc_attachments_ids_after)
    for attachment in archived_attachments:
        self.assertEqual(attachment_id_to_message_ids[attachment.id], {message.id for message in attachment.messages.all()})