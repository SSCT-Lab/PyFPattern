@pytest.mark.parametrize('np_type', [np.int8, np.int16, np.int32, np.int64])
def test_int_types(self, np_type, path):
    df = DataFrame(np.random.randint((- 10), 10, size=(10, 2)), dtype=np_type)
    df.to_excel(path, 'test1')
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    int_frame = df.astype(np.int64)
    tm.assert_frame_equal(int_frame, recons)
    recons2 = pd.read_excel(path, 'test1', index_col=0)
    tm.assert_frame_equal(int_frame, recons2)
    float_frame = df.astype(float)
    recons = pd.read_excel(path, 'test1', convert_float=False, index_col=0)
    tm.assert_frame_equal(recons, float_frame, check_index_type=False, check_column_type=False)