def batch_pix_accuracy(output, target):
    'PixAcc'
    predict = (np.argmax(output.asnumpy(), 1).astype('int64') + 1)
    target = (target.asnumpy().astype('int64') + 1)
    pixel_labeled = np.sum((target > 0))
    pixel_correct = np.sum(((predict == target) * (target > 0)))
    assert (pixel_correct <= pixel_labeled), 'Correct area should be smaller than Labeled'
    return (pixel_correct, pixel_labeled)