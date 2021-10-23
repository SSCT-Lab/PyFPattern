def create_user(self, email: str, full_name: str, is_staff: bool, date_joined: datetime, realm: Realm) -> UserProfile:
    user = UserProfile.objects.create(delivery_email=email, email=email, full_name=full_name, is_staff=is_staff, realm=realm, short_name=full_name, pointer=(- 1), last_pointer_updater='none', api_key='42', date_joined=date_joined)
    RealmAuditLog.objects.create(realm=realm, modified_user=user, event_type=RealmAuditLog.USER_CREATED, event_time=user.date_joined)
    return user