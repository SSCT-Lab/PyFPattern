@with_seed()
@unittest.skip('Flaky test, tracked in: https://github.com/apache/incubator-mxnet/issues/11747')
def test_requantize_int32_to_int8():

    def quantized_int32_to_float(qdata, min_range, max_range):
        assert (qdata.dtype == 'int32')
        quantized_range = np.iinfo('int32').max
        real_range = np.maximum(np.abs(min_range), np.abs(max_range))
        scale = (float(real_range) / float(quantized_range))
        return (qdata.astype('float32') * scale)

    def float_to_quantized_int8(data, min_range, max_range):
        assert (data.dtype == 'float32')
        real_range = np.maximum(np.abs(min_range), np.abs(max_range))
        quantized_range = np.iinfo('int8').max
        scale = (float(quantized_range) / float(real_range))
        return (np.sign(data) * np.minimum(((np.abs(data) * scale) + 0.5), quantized_range)).astype('int8')

    def requantize(qdata, min_data, max_data, real_range):
        data = quantized_int32_to_float(qdata, min_data, max_data)
        output = float_to_quantized_int8(data, (- real_range), real_range)
        return (output, (- real_range), real_range)

    def requantize_baseline(qdata, min_data, max_data, min_calib_range=None, max_calib_range=None):
        if ((min_calib_range is not None) and (max_calib_range is not None)):
            real_range = np.maximum(np.abs(min_calib_range), np.abs(max_calib_range))
            return requantize(qdata, min_data, max_data, real_range)
        else:
            min_range = quantized_int32_to_float(np.min(qdata), min_data, max_data)
            max_range = quantized_int32_to_float(np.max(qdata), min_data, max_data)
            return requantize(qdata, min_data, max_data, np.maximum(np.abs(min_range), np.abs(max_range)))

    def check_requantize(shape, min_calib_range=None, max_calib_range=None):
        qdata = mx.nd.random.uniform(low=(- 1000.0), high=1000.0, shape=shape).astype('int32')
        min_range = mx.nd.array([(- 1010.0)])
        max_range = mx.nd.array([1020.0])
        if ((min_calib_range is None) or (max_calib_range is None)):
            (qdata_int8, min_output, max_output) = mx.nd.contrib.requantize(qdata, min_range, max_range)
        else:
            (qdata_int8, min_output, max_output) = mx.nd.contrib.requantize(qdata, min_range, max_range, min_calib_range, max_calib_range)
        (qdata_int8_np, min_output_np, max_output_np) = requantize_baseline(qdata.asnumpy(), min_range.asscalar(), max_range.asscalar(), min_calib_range=min_calib_range, max_calib_range=max_calib_range)
        assert_almost_equal(qdata_int8.asnumpy(), qdata_int8_np)
        assert_almost_equal(min_output.asnumpy(), np.array([min_output_np]))
        assert_almost_equal(max_output.asnumpy(), np.array([max_output_np]))
    check_requantize((3, 4, 10, 10))
    check_requantize((32, 3, 23, 23))
    check_requantize((3, 4, 10, 10), min_calib_range=(- 1050.0), max_calib_range=1040.0)
    check_requantize((32, 3, 23, 23), min_calib_range=(- 134.349), max_calib_range=523.43)