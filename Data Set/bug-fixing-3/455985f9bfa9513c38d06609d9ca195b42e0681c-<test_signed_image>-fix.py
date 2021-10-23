def test_signed_image():
    plt.figure()
    im_signed = np.array([[(- 0.5), (- 0.2)], [0.1, 0.4]])
    with expected_warnings((imshow_expected_warnings + ['CObject type is marked|\\A\\Z'])):
        ax_im = io.imshow(im_signed)
    assert (ax_im.get_clim() == ((- 0.5), 0.5))
    assert (n_subplots(ax_im) == 2)
    assert (ax_im.colorbar is not None)