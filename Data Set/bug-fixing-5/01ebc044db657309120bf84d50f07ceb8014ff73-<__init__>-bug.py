def __init__(self, activity):
    ActivityEmail.__init__(self, activity)
    self.issues = summarize_issues(self.data['issues'])