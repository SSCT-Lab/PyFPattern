def visualize_detection(self, img, dets, classes=[], thresh=0.6):
    '\n        visualize detections in one image\n\n        Parameters:\n        ----------\n        img : numpy.array\n            image, in bgr format\n        dets : numpy.array\n            ssd detections, numpy.array([[id, score, x1, y1, x2, y2]...])\n            each row is one object\n        classes : tuple or list of str\n            class names\n        thresh : float\n            score threshold\n        '
    import matplotlib.pyplot as plt
    import random
    plt.imshow(img)
    height = img.shape[0]
    width = img.shape[1]
    colors = dict()
    for i in range(dets.shape[0]):
        cls_id = int(dets[(i, 0)])
        if (cls_id >= 0):
            score = dets[(i, 1)]
            if (score > thresh):
                if (cls_id not in colors):
                    colors[cls_id] = (random.random(), random.random(), random.random())
                xmin = int((dets[(i, 2)] * width))
                ymin = int((dets[(i, 3)] * height))
                xmax = int((dets[(i, 4)] * width))
                ymax = int((dets[(i, 5)] * height))
                rect = plt.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), fill=False, edgecolor=colors[cls_id], linewidth=3.5)
                plt.gca().add_patch(rect)
                class_name = str(cls_id)
                if (classes and (len(classes) > cls_id)):
                    class_name = classes[cls_id]
                plt.gca().text(xmin, (ymin - 2), '{:s} {:.3f}'.format(class_name, score), bbox=dict(facecolor=colors[cls_id], alpha=0.5), fontsize=12, color='white')
    plt.show()