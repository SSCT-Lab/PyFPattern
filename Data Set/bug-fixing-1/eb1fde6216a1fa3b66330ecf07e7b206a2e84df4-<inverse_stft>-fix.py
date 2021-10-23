

@tf_export('signal.inverse_stft')
def inverse_stft(stfts, frame_length, frame_step, fft_length=None, window_fn=window_ops.hann_window, name=None):
    'Computes the inverse [Short-time Fourier Transform][stft] of `stfts`.\n\n  To reconstruct an original waveform, a complimentary window function should\n  be used in inverse_stft. Such a window function can be constructed with\n  tf.signal.inverse_stft_window_fn.\n\n  Example:\n\n  ```python\n  frame_length = 400\n  frame_step = 160\n  waveform = tf.compat.v1.placeholder(dtype=tf.float32, shape=[1000])\n  stft = tf.signal.stft(waveform, frame_length, frame_step)\n  inverse_stft = tf.signal.inverse_stft(\n      stft, frame_length, frame_step,\n      window_fn=tf.signal.inverse_stft_window_fn(frame_step))\n  ```\n\n  if a custom window_fn is used in stft, it must be passed to\n  inverse_stft_window_fn:\n\n  ```python\n  frame_length = 400\n  frame_step = 160\n  window_fn = functools.partial(window_ops.hamming_window, periodic=True),\n  waveform = tf.compat.v1.placeholder(dtype=tf.float32, shape=[1000])\n  stft = tf.signal.stft(\n      waveform, frame_length, frame_step, window_fn=window_fn)\n  inverse_stft = tf.signal.inverse_stft(\n      stft, frame_length, frame_step,\n      window_fn=tf.signal.inverse_stft_window_fn(\n         frame_step, forward_window_fn=window_fn))\n  ```\n\n  Implemented with GPU-compatible ops and supports gradients.\n\n  Args:\n    stfts: A `complex64` `[..., frames, fft_unique_bins]` `Tensor` of STFT bins\n      representing a batch of `fft_length`-point STFTs where `fft_unique_bins`\n      is `fft_length // 2 + 1`\n    frame_length: An integer scalar `Tensor`. The window length in samples.\n    frame_step: An integer scalar `Tensor`. The number of samples to step.\n    fft_length: An integer scalar `Tensor`. The size of the FFT that produced\n      `stfts`. If not provided, uses the smallest power of 2 enclosing\n      `frame_length`.\n    window_fn: A callable that takes a window length and a `dtype` keyword\n      argument and returns a `[window_length]` `Tensor` of samples in the\n      provided datatype. If set to `None`, no windowing is used.\n    name: An optional name for the operation.\n\n  Returns:\n    A `[..., samples]` `Tensor` of `float32` signals representing the inverse\n    STFT for each input STFT in `stfts`.\n\n  Raises:\n    ValueError: If `stfts` is not at least rank 2, `frame_length` is not scalar,\n      `frame_step` is not scalar, or `fft_length` is not scalar.\n\n  [stft]: https://en.wikipedia.org/wiki/Short-time_Fourier_transform\n  '
    with ops.name_scope(name, 'inverse_stft', [stfts]):
        stfts = ops.convert_to_tensor(stfts, name='stfts')
        stfts.shape.with_rank_at_least(2)
        frame_length = ops.convert_to_tensor(frame_length, name='frame_length')
        frame_length.shape.assert_has_rank(0)
        frame_step = ops.convert_to_tensor(frame_step, name='frame_step')
        frame_step.shape.assert_has_rank(0)
        if (fft_length is None):
            fft_length = _enclosing_power_of_two(frame_length)
        else:
            fft_length = ops.convert_to_tensor(fft_length, name='fft_length')
            fft_length.shape.assert_has_rank(0)
        real_frames = fft_ops.irfft(stfts, [fft_length])
        frame_length_static = tensor_util.constant_value(frame_length)
        if ((frame_length_static is None) or (real_frames.shape.ndims is None) or (real_frames.shape.as_list()[(- 1)] is None)):
            real_frames = real_frames[..., :frame_length]
            real_frames_rank = array_ops.rank(real_frames)
            real_frames_shape = array_ops.shape(real_frames)
            paddings = array_ops.concat([array_ops.zeros([(real_frames_rank - 1), 2], dtype=frame_length.dtype), [[0, math_ops.maximum(0, (frame_length - real_frames_shape[(- 1)]))]]], 0)
            real_frames = array_ops.pad(real_frames, paddings)
        elif (real_frames.shape.as_list()[(- 1)] > frame_length_static):
            real_frames = real_frames[..., :frame_length_static]
        elif (real_frames.shape.as_list()[(- 1)] < frame_length_static):
            pad_amount = (frame_length_static - real_frames.shape.as_list()[(- 1)])
            real_frames = array_ops.pad(real_frames, (([[0, 0]] * (real_frames.shape.ndims - 1)) + [[0, pad_amount]]))
        if ((frame_length_static is not None) and (real_frames.shape.ndims is not None)):
            real_frames.set_shape((([None] * (real_frames.shape.ndims - 1)) + [frame_length_static]))
        if (window_fn is not None):
            window = window_fn(frame_length, dtype=stfts.dtype.real_dtype)
            real_frames *= window
        return reconstruction_ops.overlap_and_add(real_frames, frame_step)
