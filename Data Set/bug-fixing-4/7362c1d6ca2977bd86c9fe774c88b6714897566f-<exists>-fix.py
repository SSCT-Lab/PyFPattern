def exists(self):
    if (not self.want.inline):
        if os.path.exists(self.want.fulldest):
            return True
    return False