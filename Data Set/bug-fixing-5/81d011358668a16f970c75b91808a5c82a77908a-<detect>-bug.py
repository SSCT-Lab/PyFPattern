def detect(self, det_iter, show_timer=False):
    '\n        detect all images in iterator\n\n        Parameters:\n        ----------\n        det_iter : DetIter\n            iterator for all testing images\n        show_timer : Boolean\n            whether to print out detection exec time\n\n        Returns:\n        ----------\n        list of detection results\n        '
    num_images = det_iter._size
    if (not isinstance(det_iter, mx.io.PrefetchingIter)):
        det_iter = mx.io.PrefetchingIter(det_iter)
    start = timer()
    detections = self.mod.predict(det_iter).asnumpy()
    time_elapsed = (timer() - start)
    if show_timer:
        print('Detection time for {} images: {:.4f} sec'.format(num_images, time_elapsed))
    result = []
    for i in range(detections.shape[0]):
        det = detections[i, :, :]
        res = det[np.where((det[:, 0] >= 0))[0]]
        result.append(res)
    return result