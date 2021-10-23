def execute_view(self):
    for f in self.args:
        self.pager(to_text(self.editor.plaintext(f)))