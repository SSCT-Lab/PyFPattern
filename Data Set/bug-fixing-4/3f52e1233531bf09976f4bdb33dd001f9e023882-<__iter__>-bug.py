def __iter__(self):
    for text_loc in iter_dir(self.directory):
        with text_loc.open('r', encoding='utf-8') as file_:
            text = file_.read()
        (yield text)