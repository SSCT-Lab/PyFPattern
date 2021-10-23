def __gt__(self, other):
    if (self.key < other.key):
        if (self.new.enabled < other.old.enabled):
            return True
        elif (self.new.enabled > other.old.enabled):
            return False
        else:
            return (self.new.level < other.old.level)
    else:
        return (not (other > self))