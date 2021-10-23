def test_uint16():
    plt.figure()
    with expected_warnings((imshow_expected_warnings + ['CObject type is marked|\\A\\Z'])):
        ax_im = io.imshow(im16)
    assert (ax_im.cmap.name == 'gray')
    assert (ax_im.get_clim() == (0, 65535))
    assert (n_subplots(ax_im) == 1)
    assert (ax_im.colorbar is None)