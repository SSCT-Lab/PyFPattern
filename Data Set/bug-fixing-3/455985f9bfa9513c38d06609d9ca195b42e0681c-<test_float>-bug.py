def test_float():
    plt.figure()
    with expected_warnings(['tight_layout : falling back to Agg|\\A\\Z', 'CObject type is marked|\\A\\Z']):
        ax_im = io.imshow(imf)
    assert (ax_im.cmap.name == 'gray')
    assert (ax_im.get_clim() == (0, 1))
    assert (n_subplots(ax_im) == 1)
    assert (ax_im.colorbar is None)