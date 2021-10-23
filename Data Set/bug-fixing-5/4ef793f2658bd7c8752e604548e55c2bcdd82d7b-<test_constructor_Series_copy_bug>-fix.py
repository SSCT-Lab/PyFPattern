def test_constructor_Series_copy_bug(self, float_frame):
    df = DataFrame(float_frame['A'], index=float_frame.index, columns=['A'])
    df.copy()