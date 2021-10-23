def check_state(self):
    '\n        Check internal state management\n        Returns: Present if found and absent if not found\n\n        '
    return ('present' if self.vnic else 'absent')