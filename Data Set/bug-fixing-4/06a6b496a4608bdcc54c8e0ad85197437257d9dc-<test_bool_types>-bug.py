@pytest.mark.parametrize('np_type', [np.bool8, np.bool_])
def test_bool_types(self, engine, ext, np_type):
    df = DataFrame([1, 0, True, False], dtype=np_type)
    df.to_excel(self.path, 'test1')
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=0).astype(np_type)
    tm.assert_frame_equal(df, recons)