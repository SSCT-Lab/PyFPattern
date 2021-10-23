

def process_start(self):
    'Process a diff start line.'
    self.complete_file()
    match = re.search('^diff --git "?a/(?P<old_path>.*)"? "?b/(?P<new_path>.*)"?$', self.line)
    if (not match):
        raise Exception('Unexpected diff start line.')
    self.file = FileDiff(match.group('old_path'), match.group('new_path'))
    self.action = self.process_continue
