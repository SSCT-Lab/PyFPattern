def visualize_detection(self, img, dets, classes=[], thresh=0.6):
    '\n        visualize detections in one image\n\n        Parameters:\n        ----------\n        img : numpy.array\n            image, in bgr format\n        dets : numpy.array\n            ssd detections, numpy.array([[id, score, x1, y1, x2, y2]...])\n            each row is one object\n        classes : tuple or list of str\n            class names\n        thresh : float\n            score threshold\n        '
    import matplotlib.pyplot as plt
    import random
    plt.imshow(img)
    height = img.shape[0]
    width = img.shape[1]
    colors = dict()
    for det in dets:
        (klass, score, x0, y0, x1, y1) = det
        if (score < thresh):
            continue
        cls_id = int(klass)
        if (cls_id not in colors):
            colors[cls_id] = (random.random(), random.random(), random.random())
        xmin = int((x0 * width))
        ymin = int((y0 * height))
        xmax = int((x1 * width))
        ymax = int((y1 * height))
        rect = plt.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), fill=False, edgecolor=colors[cls_id], linewidth=3.5)
        plt.gca().add_patch(rect)
        class_name = str(cls_id)
        if (classes and (len(classes) > cls_id)):
            class_name = classes[cls_id]
        plt.gca().text(xmin, (ymin - 2), '{:s} {:.3f}'.format(class_name, score), bbox=dict(facecolor=colors[cls_id], alpha=0.5), fontsize=12, color='white')
    plt.show()