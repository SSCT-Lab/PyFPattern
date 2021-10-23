def get_avatar_type(self):
    if self.user_id:
        return self.user.get_avatar_type()
    return 'letter_avatar'