def convert_avatar_data(avatar_folder: str, raw_data: List[ZerverFieldsT], realm_id: int) -> List[ZerverFieldsT]:
    "\n    This code is pretty specific to how Hipchat sends us data.\n    They give us the avatar payloads in base64 in users.json.\n\n    We process avatars in our own pass of that data, rather\n    than doing it while we're getting other user data.  I\n    chose to keep this separate, as otherwise you have a lot\n    of extraneous data getting passed around.\n\n    This code has MAJOR SIDE EFFECTS--namely writing a bunch\n    of files to the avatars directory.\n    "
    flat_data = [d['User'] for d in raw_data]

    def process(raw_user: ZerverFieldsT) -> ZerverFieldsT:
        avatar_payload = raw_user['avatar']
        bits = base64.b64decode(avatar_payload)
        user_id = raw_user['id']
        metadata = write_avatar_png(avatar_folder=avatar_folder, realm_id=realm_id, user_id=user_id, bits=bits)
        return metadata
    avatar_records = list(map(process, flat_data))
    return avatar_records