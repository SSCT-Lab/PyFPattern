def log(self, msg, pretty_print=False):
    if pretty_print:
        self.module.debug(json.dumps(msg, indent=4, sort_keys=True))
    else:
        self.module.debug(msg)