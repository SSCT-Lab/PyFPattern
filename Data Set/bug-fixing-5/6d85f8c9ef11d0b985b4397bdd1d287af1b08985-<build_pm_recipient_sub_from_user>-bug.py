def build_pm_recipient_sub_from_user(zulip_user_id: int, recipient_id: int, subscription_id: int) -> Tuple[(ZerverFieldsT, ZerverFieldsT)]:
    recipient = dict(type_id=zulip_user_id, id=recipient_id, type=1)
    sub = dict(recipient=recipient_id, notifications=False, color='#c2c2c2', desktop_notifications=True, pin_to_top=False, in_home_view=True, active=True, user_profile=zulip_user_id, id=subscription_id)
    return (recipient, sub)