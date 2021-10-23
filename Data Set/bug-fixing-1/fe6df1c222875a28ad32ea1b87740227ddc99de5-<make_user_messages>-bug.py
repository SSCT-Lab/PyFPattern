

def make_user_messages(zerver_message: List[ZerverFieldsT], subscriber_map: Dict[(int, Set[int])], mention_map: Dict[(int, Set[int])]) -> List[ZerverFieldsT]:
    zerver_usermessage = []
    for message in zerver_message:
        message_id = message['id']
        recipient_id = message['recipient']
        sender_id = message['sender']
        mention_user_ids = mention_map[message_id]
        user_ids = subscriber_map.get(recipient_id, set())
        user_ids.add(sender_id)
        for user_id in user_ids:
            is_mentioned = (user_id in mention_user_ids)
            user_message = build_user_message(id=NEXT_ID('user_message'), user_id=user_id, message_id=message_id, is_mentioned=is_mentioned)
            zerver_usermessage.append(user_message)
    return zerver_usermessage
