def test_read_fail():
    for mmap in [False, True]:
        fp = open(datafile('example_1.nc'))
        assert_raises(ValueError, wavfile.read, fp, mmap=mmap)
        fp.close()