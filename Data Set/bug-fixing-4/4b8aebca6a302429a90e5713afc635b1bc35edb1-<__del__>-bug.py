def __del__(self):
    '\n        Automatic destructor which closes the underlying file.\n\n        There must be no circular references contained in the object for __del__\n        to work! Closing the file explicitly via the close() method is preferred\n        and safer.\n        '
    self.close()