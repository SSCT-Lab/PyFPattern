def convert_user_data(raw_data: List[ZerverFieldsT], realm_id: int) -> List[ZerverFieldsT]:
    flat_data = [d['User'] for d in raw_data]

    def process(in_dict: ZerverFieldsT) -> ZerverFieldsT:
        delivery_email = in_dict['email']
        email = in_dict['email']
        full_name = in_dict['name']
        id = in_dict['id']
        is_realm_admin = (in_dict['account_type'] == 'admin')
        is_guest = (in_dict['account_type'] == 'guest')
        short_name = in_dict['mention_name']
        timezone = in_dict['timezone']
        date_joined = int(timezone_now().timestamp())
        is_active = (not in_dict['is_deleted'])
        return build_user(avatar_source='U', date_joined=date_joined, delivery_email=delivery_email, email=email, full_name=full_name, id=id, is_active=is_active, is_realm_admin=is_realm_admin, is_guest=is_guest, realm_id=realm_id, short_name=short_name, timezone=timezone)
    return list(map(process, flat_data))