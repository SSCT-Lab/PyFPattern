def build_subscription(channel_members: List[str], zerver_subscription: List[ZerverFieldsT], recipient_id: int, added_users: AddedUsersT, subscription_id_list: List[int], subscription_id_count: int) -> int:
    for member in channel_members:
        subscription_id = subscription_id_list[subscription_id_count]
        sub = dict(recipient=recipient_id, notifications=False, color='#c2c2c2', desktop_notifications=True, pin_to_top=False, in_home_view=True, active=True, user_profile=added_users[member], id=subscription_id)
        zerver_subscription.append(sub)
        subscription_id_count += 1
    return subscription_id_count