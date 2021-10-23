@testing.skipif((not imageio_available), reason='imageio not installed')
def test_imageio_flatten():
    img = imread(os.path.join(data_dir, 'color.png'), flatten=True)
    assert (img.ndim == 2)
    assert (img.dtype == np.float64)
    img = imread(os.path.join(data_dir, 'camera.png'), flatten=True)
    assert (np.sctype2char(img.dtype) in np.typecodes['AllInteger'])