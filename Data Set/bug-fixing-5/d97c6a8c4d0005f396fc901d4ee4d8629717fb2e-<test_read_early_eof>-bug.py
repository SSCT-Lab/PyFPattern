def test_read_early_eof():
    for mmap in [False, True]:
        fp = open(datafile('test-44100Hz-le-1ch-4bytes-early-eof.wav'))
        assert_raises(ValueError, wavfile.read, fp, mmap=mmap)
        fp.close()