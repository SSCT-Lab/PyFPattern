def test_eng_float_formatter(self):
    self.frame.loc[5] = 0
    fmt.set_eng_float_format()
    repr(self.frame)
    fmt.set_eng_float_format(use_eng_prefix=True)
    repr(self.frame)
    fmt.set_eng_float_format(accuracy=0)
    repr(self.frame)
    tm.reset_display_options()