def test_outside_standard_range():
    plt.figure()
    with expected_warnings((imshow_expected_warnings + ['out of standard range|CObject type is marked'])):
        ax_im = io.imshow(im_hi)
    assert (ax_im.get_clim() == (im_hi.min(), im_hi.max()))
    assert (n_subplots(ax_im) == 2)
    assert (ax_im.colorbar is not None)