@pytest.mark.backend('pdf')
def test_non_gui_warning(monkeypatch):
    plt.subplots()
    monkeypatch.setitem(os.environ, 'DISPLAY', ':999')
    with pytest.warns(UserWarning) as rec:
        plt.show()
        assert (len(rec) == 1)
        assert ('Matplotlib is currently using pdf, which is a non-GUI backend' in str(rec[0].message))
    with pytest.warns(UserWarning) as rec:
        plt.gcf().show()
        assert (len(rec) == 1)
        assert ('Matplotlib is currently using pdf, which is a non-GUI backend' in str(rec[0].message))