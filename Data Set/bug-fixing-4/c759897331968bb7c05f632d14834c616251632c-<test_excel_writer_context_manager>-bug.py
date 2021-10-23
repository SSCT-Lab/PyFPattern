def test_excel_writer_context_manager(self, frame, frame2, *_):
    with ExcelWriter(self.path) as writer:
        frame.to_excel(writer, 'Data1')
        frame2.to_excel(writer, 'Data2')
    with ExcelFile(self.path) as reader:
        found_df = pd.read_excel(reader, 'Data1', index_col=0)
        found_df2 = pd.read_excel(reader, 'Data2', index_col=0)
        tm.assert_frame_equal(found_df, frame)
        tm.assert_frame_equal(found_df2, frame2)