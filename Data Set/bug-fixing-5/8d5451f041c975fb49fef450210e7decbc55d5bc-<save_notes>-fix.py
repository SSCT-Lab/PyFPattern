def save_notes(self):
    with open(self.notes_fn, 'w') as fd:
        json.dump(self.notes.data, fd)