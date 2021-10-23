def check_tag_status(self):
    "\n        Function to check if tag exists or not\n        Returns: 'present' if tag found, else 'absent'\n\n        "
    if (self.tag_name in self.global_tags):
        return 'present'
    else:
        return 'absent'