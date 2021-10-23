def set_object_info(self):
    ' set my pandas type & version '
    self.attrs.pandas_type = str(self.pandas_kind)
    self.attrs.pandas_version = str(_version)
    self.set_version()