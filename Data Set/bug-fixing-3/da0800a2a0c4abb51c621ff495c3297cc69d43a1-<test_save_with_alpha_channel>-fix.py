def test_save_with_alpha_channel():
    pic = novice.Picture(array=np.zeros((3, 3, 4)))
    (fd, filename) = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    pic.save(filename)
    os.unlink(filename)