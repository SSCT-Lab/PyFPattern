def ensure_state(self):
    '\n        Manage internal states of tags\n\n        '
    desired_state = self.params.get('state')
    states = {
        'present': {
            'present': self.state_update_tag,
            'absent': self.state_create_tag,
        },
        'absent': {
            'present': self.state_delete_tag,
            'absent': self.state_unchanged,
        },
    }
    states[desired_state][self.check_tag_status()]()