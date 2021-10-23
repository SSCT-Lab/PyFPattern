def test_read_incomplete_chunk():
    for mmap in [False, True]:
        fp = open(datafile('test-44100Hz-le-1ch-4bytes-incomplete-chunk.wav'))
        assert_raises(ValueError, wavfile.read, fp, mmap=mmap)
        fp.close()