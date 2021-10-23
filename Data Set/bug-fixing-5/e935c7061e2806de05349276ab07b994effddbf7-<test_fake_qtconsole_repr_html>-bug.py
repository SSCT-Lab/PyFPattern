def test_fake_qtconsole_repr_html(self):

    def get_ipython():
        return {
            'config': {
                'KernelApp': {
                    'parent_appname': 'ipython-qtconsole',
                },
            },
        }
    repstr = self.frame._repr_html_()
    assert (repstr is not None)
    fmt.set_option('display.max_rows', 5, 'display.max_columns', 2)
    repstr = self.frame._repr_html_()
    assert ('class' in repstr)
    tm.reset_display_options()