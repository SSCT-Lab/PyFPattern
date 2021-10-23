

def populate_filesystems(self):
    data = self.responses[0]
    if isinstance(data, dict):
        data = data['messages'][0]
    fs = re.findall('^Directory of (.+)/', data, re.M)
    return dict(filesystems=fs)
