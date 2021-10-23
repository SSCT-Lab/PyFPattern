def get_device_operations(self):
    return {
        'supports_diff_replace': True,
        'supports_commit': False,
        'supports_rollback': False,
        'supports_defaults': True,
        'supports_onbox_diff': False,
        'supports_commit_comment': False,
        'supports_multiline_delimiter': False,
        'supports_diff_match': True,
        'supports_diff_ignore_lines': True,
        'supports_generate_diff': True,
        'supports_replace': False,
    }