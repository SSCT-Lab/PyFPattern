def debugl(self, text):
    if self.args.debug:
        try:
            text = str(text)
        except UnicodeEncodeError:
            text = text.encode('ascii', 'ignore')
        print(text)