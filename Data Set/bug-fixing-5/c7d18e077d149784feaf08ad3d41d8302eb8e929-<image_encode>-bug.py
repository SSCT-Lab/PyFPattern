def image_encode(args, i, item, q_out):
    fullpath = os.path.join(args.root, item[1])
    if ((len(item) > 3) and args.pack_label):
        header = mx.recordio.IRHeader(0, item[2:], item[0], 0)
    else:
        header = mx.recordio.IRHeader(0, item[2], item[0], 0)
    if args.pass_through:
        try:
            with open(fullpath, 'rb') as fin:
                img = fin.read()
            s = mx.recordio.pack(header, img)
            q_out.put((i, s, item))
        except Exception as e:
            traceback.print_exc()
            print('pack_img error:', item[1], e)
            q_out.put((i, None, item))
        return
    try:
        img = cv2.imread(fullpath, args.color)
    except:
        traceback.print_exc()
        print(('imread error trying to load file: %s ' % fullpath))
        q_out.put((i, None, item))
        return
    if (img is None):
        print(('imread read blank (None) image for file: %s' % fullpath))
        q_out.put((i, None, item))
        return
    if args.center_crop:
        if (img.shape[0] > img.shape[1]):
            margin = ((img.shape[0] - img.shape[1]) / 2)
            img = img[margin:(margin + img.shape[1]), :]
        else:
            margin = ((img.shape[1] - img.shape[0]) / 2)
            img = img[:, margin:(margin + img.shape[0])]
    if args.resize:
        if (img.shape[0] > img.shape[1]):
            newsize = (args.resize, ((img.shape[0] * args.resize) / img.shape[1]))
        else:
            newsize = (((img.shape[1] * args.resize) / img.shape[0]), args.resize)
        img = cv2.resize(img, newsize)
    try:
        s = mx.recordio.pack_img(header, img, quality=args.quality, img_fmt=args.encoding)
        q_out.put((i, s, item))
    except Exception as e:
        traceback.print_exc()
        print(('pack_img error on file: %s' % fullpath), e)
        q_out.put((i, None, item))
        return