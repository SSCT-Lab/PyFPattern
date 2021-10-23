def test_low_data_range():
    with expected_warnings((imshow_expected_warnings + ['Low image data range|CObject type is marked'])):
        ax_im = io.imshow(im_lo)
    assert (ax_im.get_clim() == (im_lo.min(), im_lo.max()))
    assert (ax_im.colorbar is not None)