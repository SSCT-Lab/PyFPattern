def test_fake_qtconsole_repr_html(self, float_frame):
    df = float_frame

    def get_ipython():
        return {
            'config': {
                'KernelApp': {
                    'parent_appname': 'ipython-qtconsole',
                },
            },
        }
    repstr = df._repr_html_()
    assert (repstr is not None)
    fmt.set_option('display.max_rows', 5, 'display.max_columns', 2)
    repstr = df._repr_html_()
    assert ('class' in repstr)
    tm.reset_display_options()