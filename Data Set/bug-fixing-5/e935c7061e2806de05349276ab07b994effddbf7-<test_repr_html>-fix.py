def test_repr_html(self, float_frame):
    df = float_frame
    df._repr_html_()
    fmt.set_option('display.max_rows', 1, 'display.max_columns', 1)
    df._repr_html_()
    fmt.set_option('display.notebook_repr_html', False)
    df._repr_html_()
    tm.reset_display_options()
    df = DataFrame([[1, 2], [3, 4]])
    fmt.set_option('display.show_dimensions', True)
    assert ('2 rows' in df._repr_html_())
    fmt.set_option('display.show_dimensions', False)
    assert ('2 rows' not in df._repr_html_())
    tm.reset_display_options()