def test_nonstandard_type():
    plt.figure()
    with expected_warnings(['Low image data range|CObject type is marked', 'tight_layout : falling back to Agg|\\A\\Z']):
        ax_im = io.imshow(im64)
    assert (ax_im.get_clim() == (im64.min(), im64.max()))
    assert (n_subplots(ax_im) == 2)
    assert (ax_im.colorbar is not None)