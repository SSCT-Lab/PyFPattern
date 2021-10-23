@pytest.mark.backend('pdf')
@pytest.mark.skipif(('SYSTEM_TEAMFOUNDATIONCOLLECTIONURI' in os.environ), reason='this test fails an azure for unknown reasons')
def test_non_gui_warning():
    plt.subplots()
    with pytest.warns(UserWarning) as rec:
        plt.show()
        assert (len(rec) == 1)
        assert ('Matplotlib is currently using pdf, which is a non-GUI backend' in str(rec[0].message))
    with pytest.warns(UserWarning) as rec:
        plt.gcf().show()
        assert (len(rec) == 1)
        assert ('Matplotlib is currently using pdf, which is a non-GUI backend' in str(rec[0].message))