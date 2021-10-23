def test_eng_float_formatter(self, float_frame):
    df = float_frame
    df.loc[5] = 0
    fmt.set_eng_float_format()
    repr(df)
    fmt.set_eng_float_format(use_eng_prefix=True)
    repr(df)
    fmt.set_eng_float_format(accuracy=0)
    repr(df)
    tm.reset_display_options()