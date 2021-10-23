def test_constructor_Series_copy_bug(self):
    df = DataFrame(self.frame['A'], index=self.frame.index, columns=['A'])
    df.copy()