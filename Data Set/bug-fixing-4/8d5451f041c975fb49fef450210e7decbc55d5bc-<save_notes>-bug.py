def save_notes(self):
    with open(self.notes_fn, 'wb') as fd:
        json.dump(self.notes.data, fd)