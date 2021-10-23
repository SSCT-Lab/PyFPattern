def __exit__(self, exc_type, exc_value, traceback):
    super().__exit__(exc_type, exc_value, traceback)
    self.connection.check_constraints()
    self.connection.enable_constraint_checking()