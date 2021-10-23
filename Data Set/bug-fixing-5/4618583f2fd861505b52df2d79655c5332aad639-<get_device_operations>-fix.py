def get_device_operations(self):
    return {
        'supports_diff_replace': True,
        'supports_commit': (True if self.supports_sessions else False),
        'supports_rollback': (True if self.supports_sessions else False),
        'supports_defaults': False,
        'supports_onbox_diff': (True if self.supports_sessions else False),
        'supports_commit_comment': False,
        'supports_multiline_delimiter': False,
        'supports_diff_match': True,
        'supports_diff_ignore_lines': True,
        'supports_generate_diff': (False if self.supports_sessions else True),
        'supports_replace': (True if self.supports_sessions else False),
    }