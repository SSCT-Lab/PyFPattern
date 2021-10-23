def execute_view(self):
    for f in self.args:
        self.pager(ansible.module_utils._text.to_text(self.editor.plaintext(f)))