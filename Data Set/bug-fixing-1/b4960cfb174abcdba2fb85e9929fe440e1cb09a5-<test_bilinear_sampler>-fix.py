

def test_bilinear_sampler():
    from math import floor

    def between(x, lowerbound, upperbound):
        return ((x >= lowerbound) and (x <= upperbound))

    def bilinear_forward_numpy(data, grid):
        batchsize = data.shape[0]
        input_height = data.shape[2]
        input_width = data.shape[3]
        num_channel = data.shape[1]
        output_height = grid.shape[2]
        output_width = grid.shape[3]
        out = np.zeros((data.shape[:2] + grid.shape[2:]), dtype=np.float32)
        for i in range(batchsize):
            for yout in range(output_height):
                for xout in range(output_width):
                    xcoord = np.float32((((grid[(i, 0, yout, xout)] + 1) * (input_width - 1)) / 2.0))
                    ycoord = np.float32((((grid[(i, 1, yout, xout)] + 1) * (input_height - 1)) / 2.0))
                    xInTopLeft = int(floor(xcoord))
                    xWeightTopLeft = np.float32((1 - (xcoord - xInTopLeft)))
                    yInTopLeft = int(floor(ycoord))
                    yWeightTopLeft = np.float32((1 - (ycoord - yInTopLeft)))
                    for channel in range(num_channel):
                        inTopLeft = (data[(i, channel, yInTopLeft, xInTopLeft)] if (between(xInTopLeft, 0, (input_width - 1)) and between(yInTopLeft, 0, (input_height - 1))) else 0.0)
                        inTopRight = (data[(i, channel, yInTopLeft, (xInTopLeft + 1))] if (between((xInTopLeft + 1), 0, (input_width - 1)) and between(yInTopLeft, 0, (input_height - 1))) else 0.0)
                        inBottomLeft = (data[(i, channel, (yInTopLeft + 1), xInTopLeft)] if (between(xInTopLeft, 0, (input_width - 1)) and between((yInTopLeft + 1), 0, (input_height - 1))) else 0.0)
                        inBottomRight = (data[(i, channel, (yInTopLeft + 1), (xInTopLeft + 1))] if (between((xInTopLeft + 1), 0, (input_width - 1)) and between((yInTopLeft + 1), 0, (input_height - 1))) else 0.0)
                        out[(i, channel, yout, xout)] = (((((xWeightTopLeft * yWeightTopLeft) * inTopLeft) + (((1 - xWeightTopLeft) * yWeightTopLeft) * inTopRight)) + ((xWeightTopLeft * (1 - yWeightTopLeft)) * inBottomLeft)) + (((1 - xWeightTopLeft) * (1 - yWeightTopLeft)) * inBottomRight))
        return out

    def bilinear_backward_numpy(out_grad, data, grid):
        data_grad = np.zeros(data.shape, dtype=np.float32)
        grid_grad = np.zeros(grid.shape, dtype=np.float32)
        batchsize = data.shape[0]
        input_height = data.shape[2]
        input_width = data.shape[3]
        num_channel = data.shape[1]
        output_height = grid.shape[2]
        output_width = grid.shape[3]
        for i in range(batchsize):
            for yout in range(output_height):
                for xout in range(output_width):
                    top_left_y_gw = np.float32(0.0)
                    top_left_x_gw = np.float32(0.0)
                    xcoord = np.float32((((grid[(i, 0, yout, xout)] + 1) * (input_width - 1)) / 2.0))
                    ycoord = np.float32((((grid[(i, 1, yout, xout)] + 1) * (input_height - 1)) / 2.0))
                    xInTopLeft = int(floor(xcoord))
                    xWeightTopLeft = np.float32((1 - (xcoord - xInTopLeft)))
                    yInTopLeft = int(floor(ycoord))
                    yWeightTopLeft = np.float32((1 - (ycoord - yInTopLeft)))
                    topLeftDotProduct = np.float32(0)
                    topRightDotProduct = np.float32(0)
                    bottomLeftDotProduct = np.float32(0)
                    bottomRightDotProduct = np.float32(0)
                    for channel in range(num_channel):
                        if (between(xInTopLeft, 0, (input_width - 1)) and between(yInTopLeft, 0, (input_height - 1))):
                            topLeftDotProduct += (data[(i, channel, yInTopLeft, xInTopLeft)] * out_grad[(i, channel, yout, xout)])
                            data_grad[(i, channel, yInTopLeft, xInTopLeft)] += ((xWeightTopLeft * yWeightTopLeft) * out_grad[(i, channel, yout, xout)])
                        if (between((xInTopLeft + 1), 0, (input_width - 1)) and between(yInTopLeft, 0, (input_height - 1))):
                            topRightDotProduct += (data[(i, channel, yInTopLeft, (xInTopLeft + 1))] * out_grad[(i, channel, yout, xout)])
                            data_grad[(i, channel, yInTopLeft, (xInTopLeft + 1))] += (((1 - xWeightTopLeft) * yWeightTopLeft) * out_grad[(i, channel, yout, xout)])
                        if (between(xInTopLeft, 0, (input_width - 1)) and between((yInTopLeft + 1), 0, (input_height - 1))):
                            bottomLeftDotProduct += (data[(i, channel, (yInTopLeft + 1), xInTopLeft)] * out_grad[(i, channel, yout, xout)])
                            data_grad[(i, channel, (yInTopLeft + 1), xInTopLeft)] += ((xWeightTopLeft * (1 - yWeightTopLeft)) * out_grad[(i, channel, yout, xout)])
                        if (between((xInTopLeft + 1), 0, (input_width - 1)) and between((yInTopLeft + 1), 0, (input_height - 1))):
                            bottomRightDotProduct += (data[(i, channel, (yInTopLeft + 1), (xInTopLeft + 1))] * out_grad[(i, channel, yout, xout)])
                            data_grad[(i, channel, (yInTopLeft + 1), (xInTopLeft + 1))] += (((1 - xWeightTopLeft) * (1 - yWeightTopLeft)) * out_grad[(i, channel, yout, xout)])
                    yf = np.float32((((((- xWeightTopLeft) * topLeftDotProduct) + (xWeightTopLeft * bottomLeftDotProduct)) - ((1 - xWeightTopLeft) * topRightDotProduct)) + ((1 - xWeightTopLeft) * bottomRightDotProduct)))
                    xf = np.float32((((((- yWeightTopLeft) * topLeftDotProduct) + (yWeightTopLeft * topRightDotProduct)) - ((1 - yWeightTopLeft) * bottomLeftDotProduct)) + ((1 - yWeightTopLeft) * bottomRightDotProduct)))
                    grid_grad[(i, 0, yout, xout)] = ((xf * (input_width - 1)) / 2.0)
                    grid_grad[(i, 1, yout, xout)] = ((yf * (input_height - 1)) / 2.0)
        return (data_grad, grid_grad)
    data = mx.sym.Variable('data')
    grid = mx.sym.Variable('grid')
    net = mx.sym.BilinearSampler(data=data, grid=grid)
    test_case = [[(1, 3, 15, 16), (1, 2, 10, 10)], [(1, 6, 7, 16), (1, 2, 10, 4)], [(1, 7, 3, 16), (1, 2, 8, 11)], [(1, 9, 50, 50), (1, 2, 50, 50)]]
    for ctx in [default_context()]:
        for item in test_case:
            (data_shape, grid_shape) = item
            exe = net.simple_bind(data=data_shape, grid=grid_shape, ctx=ctx, grad_req='write')
            exe.arg_dict['data'][:] = np.random.uniform(low=(- 0.1), high=0.1, size=data_shape).astype(np.float32)
            exe.arg_dict['grid'][:] = np.random.uniform(low=(- 2), high=2, size=grid_shape).astype(np.float32)
            exe.forward()
            out = bilinear_forward_numpy(exe.arg_dict['data'].asnumpy(), exe.arg_dict['grid'].asnumpy())
            assert_almost_equal(exe.outputs[0].asnumpy(), out, rtol=0.001, atol=1e-05)
            out_grad = np.random.uniform(low=(- 0.01), high=0.01, size=(data_shape[:2] + grid_shape[2:])).astype(np.float32)
            exe.backward(mx.nd.array(out_grad))
            (data_grad, grid_grad) = bilinear_backward_numpy(out_grad, exe.arg_dict['data'].asnumpy(), exe.arg_dict['grid'].asnumpy())
            assert_almost_equal(exe.grad_dict['data'].asnumpy(), data_grad, rtol=0.001, atol=1e-05)
            assert_almost_equal(exe.grad_dict['grid'].asnumpy(), grid_grad, rtol=0.001, atol=1e-05)
            exe_addto = net.simple_bind(data=data_shape, grid=grid_shape, ctx=ctx, grad_req='add')
            data_initial_grid = np.random.normal(size=exe_addto.grad_dict['data'].shape).astype(np.float32)
            grid_initial_grid = np.random.normal(size=exe_addto.grad_dict['grid'].shape).astype(np.float32)
            exe_addto.arg_dict['data'][:] = exe.arg_dict['data'][:]
            exe_addto.arg_dict['grid'][:] = exe.arg_dict['grid'][:]
            exe_addto.grad_dict['data'][:] = data_initial_grid
            exe_addto.grad_dict['grid'][:] = grid_initial_grid
            exe_addto.forward()
            exe_addto.backward(mx.nd.array(out_grad))
            assert_almost_equal(exe_addto.grad_dict['data'].asnumpy(), (data_grad + data_initial_grid), rtol=0.001, atol=1e-05)
            assert_almost_equal(exe_addto.grad_dict['grid'].asnumpy(), (grid_grad + grid_initial_grid), rtol=0.001, atol=1e-05)
