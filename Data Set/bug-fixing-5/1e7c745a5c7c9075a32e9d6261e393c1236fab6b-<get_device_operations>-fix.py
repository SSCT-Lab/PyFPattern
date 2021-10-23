def get_device_operations(self):
    return {
        'supports_diff_replace': False,
        'supports_commit': True,
        'supports_rollback': False,
        'supports_defaults': False,
        'supports_onbox_diff': True,
        'supports_commit_comment': True,
        'supports_multiline_delimiter': False,
        'supports_diff_match': True,
        'supports_diff_ignore_lines': False,
        'supports_generate_diff': False,
        'supports_replace': False,
    }