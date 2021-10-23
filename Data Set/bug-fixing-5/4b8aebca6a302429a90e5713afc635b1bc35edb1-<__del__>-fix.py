def __del__(self):
    'Automatic destructor which closes the underlying file.\n\n        Notes\n        -----\n        There must be no circular references contained in the object for __del__ to work!\n        Closing the file explicitly via the close() method is preferred and safer.\n\n        '
    self.close()