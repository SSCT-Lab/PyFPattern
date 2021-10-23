def detect_and_visualize(self, im_list, root_dir=None, extension=None, classes=[], thresh=0.6, show_timer=False):
    '\n        wrapper for im_detect and visualize_detection\n\n        Parameters:\n        ----------\n        im_list : list of str or str\n            image path or list of image paths\n        root_dir : str or None\n            directory of input images, optional if image path already\n            has full directory information\n        extension : str or None\n            image extension, eg. ".jpg", optional\n\n        Returns:\n        ----------\n\n        '
    import cv2
    dets = self.im_detect(im_list, root_dir, extension, show_timer=show_timer)
    if (not isinstance(im_list, list)):
        im_list = [im_list]
    assert (len(dets) == len(im_list))
    for (k, det) in enumerate(dets):
        img = cv2.imread(im_list[k])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.visualize_detection(img, det, classes, thresh)