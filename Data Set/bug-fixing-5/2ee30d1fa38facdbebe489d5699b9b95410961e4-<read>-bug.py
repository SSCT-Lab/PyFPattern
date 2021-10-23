def read(filename, mmap=False):
    '\n    Open a WAV file\n\n    Return the sample rate (in samples/sec) and data from a WAV file.\n\n    Parameters\n    ----------\n    filename : string or open file handle\n        Input wav file.\n    mmap : bool, optional\n        Whether to read data as memory-mapped.\n        Only to be used on real files (Default: False).\n\n        .. versionadded:: 0.12.0\n\n    Returns\n    -------\n    rate : int\n        Sample rate of wav file.\n    data : numpy array\n        Data read from wav file. Data-type is determined from the file;\n        see Notes.\n\n    Notes\n    -----\n    This function cannot read wav files with 24-bit data.\n\n    Common data types: [1]_\n\n    =====================  ===========  ===========  =============\n         WAV format            Min          Max       NumPy dtype\n    =====================  ===========  ===========  =============\n    32-bit floating-point  -1.0         +1.0         float32\n    32-bit PCM             -2147483648  +2147483647  int32\n    16-bit PCM             -32768       +32767       int16\n    8-bit PCM              0            255          uint8\n    =====================  ===========  ===========  =============\n\n    Note that 8-bit PCM is unsigned.\n\n    References\n    ----------\n    .. [1] IBM Corporation and Microsoft Corporation, "Multimedia Programming\n       Interface and Data Specifications 1.0", section "Data Format of the\n       Samples", August 1991\n       http://www.tactilemedia.com/info/MCI_Control_Info.html\n\n    Examples\n    --------\n    >>> from os.path import dirname, join as pjoin\n    >>> import scipy.io as sio\n\n    Get the filename for an example .wav file from the tests/data directory.\n\n    >>> data_dir = pjoin(dirname(sio.__file__), \'tests\', \'data\')\n    >>> wav_fname = pjoin(data_dir, \'test-44100Hz-2ch-32bit-float-be.wav\')\n\n    Load the .wav file contents.\n\n    >>> samplerate, data = sio.wavfile.read(wav_fname)\n    >>> print(f"number of channels = {data.shape[1]}")\n    number of channels = 2\n    >>> length = data.shape[0] / samplerate\n    >>> print(f"length = {length}s")\n    length = 0.01s\n\n    Plot the waveform.\n\n    >>> import matplotlib.pyplot as plt\n    >>> import numpy as np\n    >>> time = np.linspace(0., length, data.shape[0])\n    >>> plt.plot(time, data[:, 0], label="Left channel")\n    >>> plt.plot(time, data[:, 1], label="Right channel")\n    >>> plt.legend()\n    >>> plt.xlabel("Time [s]")\n    >>> plt.ylabel("Amplitude")\n    >>> plt.show()\n\n    '
    if hasattr(filename, 'read'):
        fid = filename
        mmap = False
    else:
        fid = open(filename, 'rb')
    try:
        (file_size, is_big_endian) = _read_riff_chunk(fid)
        fmt_chunk_received = False
        data_chunk_received = False
        channels = 1
        bit_depth = 8
        format_tag = WAVE_FORMAT_PCM
        while (fid.tell() < file_size):
            chunk_id = fid.read(4)
            if (not chunk_id):
                if data_chunk_received:
                    warnings.warn('Reached EOF prematurely; finished at {:d} bytes, expected {:d} bytes from header.'.format(fid.tell(), file_size), WavFileWarning, stacklevel=2)
                    break
                else:
                    raise ValueError('Unexpected end of file.')
            elif (len(chunk_id) < 4):
                raise ValueError('Incomplete wav chunk.')
            if (chunk_id == b'fmt '):
                fmt_chunk_received = True
                fmt_chunk = _read_fmt_chunk(fid, is_big_endian)
                (format_tag, channels, fs) = fmt_chunk[1:4]
                bit_depth = fmt_chunk[6]
                if (bit_depth not in (8, 16, 32, 64, 96, 128)):
                    raise ValueError('Unsupported bit depth: the wav file has {}-bit data.'.format(bit_depth))
            elif (chunk_id == b'fact'):
                _skip_unknown_chunk(fid, is_big_endian)
            elif (chunk_id == b'data'):
                data_chunk_received = True
                if (not fmt_chunk_received):
                    raise ValueError('No fmt chunk before data')
                data = _read_data_chunk(fid, format_tag, channels, bit_depth, is_big_endian, mmap)
            elif (chunk_id == b'LIST'):
                _skip_unknown_chunk(fid, is_big_endian)
            elif (chunk_id in (b'JUNK', b'Fake')):
                _skip_unknown_chunk(fid, is_big_endian)
            else:
                warnings.warn('Chunk (non-data) not understood, skipping it.', WavFileWarning, stacklevel=2)
                _skip_unknown_chunk(fid, is_big_endian)
    finally:
        if (not hasattr(filename, 'read')):
            fid.close()
        else:
            fid.seek(0)
    return (fs, data)