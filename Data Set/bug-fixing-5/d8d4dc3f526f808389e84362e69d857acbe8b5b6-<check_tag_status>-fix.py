def check_tag_status(self):
    "\n        Check if tag exists or not\n        Returns: 'present' if tag found, else 'absent'\n\n        "
    ret = ('present' if (self.tag_name in self.global_tags) else 'absent')
    return ret