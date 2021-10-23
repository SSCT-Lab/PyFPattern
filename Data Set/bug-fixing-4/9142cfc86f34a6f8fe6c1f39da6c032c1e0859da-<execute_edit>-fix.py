def execute_edit(self):
    ' open and decrypt an existing vaulted file in an editor, that will be encrypted again when closed'
    for f in self.args:
        self.editor.edit_file(f)