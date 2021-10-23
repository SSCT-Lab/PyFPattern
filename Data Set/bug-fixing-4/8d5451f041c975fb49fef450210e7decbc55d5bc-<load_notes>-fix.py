def load_notes(self):
    if (not exists(self.notes_fn)):
        return
    with open(self.notes_fn) as fd:
        data = json.load(fd)
    self.notes.data = data