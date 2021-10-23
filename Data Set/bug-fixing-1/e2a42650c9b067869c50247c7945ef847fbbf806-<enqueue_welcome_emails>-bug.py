

def enqueue_welcome_emails(user: UserProfile) -> None:
    from zerver.context_processors import common_context
    if (settings.WELCOME_EMAIL_SENDER is not None):
        from_name = settings.WELCOME_EMAIL_SENDER['name']
        from_address = settings.WELCOME_EMAIL_SENDER['email']
    else:
        from_name = None
        from_address = FromAddress.SUPPORT
    unsubscribe_link = one_click_unsubscribe_link(user, 'welcome')
    context = common_context(user)
    context.update({
        'unsubscribe_link': unsubscribe_link,
        'organization_setup_advice_link': (user.realm.uri + '%s/help/getting-your-organization-started-with-zulip'),
        'is_realm_admin': user.is_realm_admin,
    })
    send_future_email('zerver/emails/followup_day1', user.realm, to_user_id=user.id, from_name=from_name, from_address=from_address, context=context)
    send_future_email('zerver/emails/followup_day2', user.realm, to_user_id=user.id, from_name=from_name, from_address=from_address, context=context, delay=datetime.timedelta(days=1))
