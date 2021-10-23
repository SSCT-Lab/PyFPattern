def test(model, args, input_transform):
    outdir = 'outdir'
    if (not os.path.exists(outdir)):
        os.makedirs(outdir)
    if args.eval:
        testset = get_segmentation_dataset(args.dataset, split='val', mode='testval', transform=input_transform)
        (total_inter, total_union, total_correct, total_label) = (np.int64(0), np.int64(0), np.int64(0), np.int64(0))
    else:
        testset = get_segmentation_dataset(args.dataset, split='test', mode='test', transform=input_transform)
    test_data = gluon.data.DataLoader(testset, args.batch_size, shuffle=False, last_batch='keep', batchify_fn=ms_batchify_fn, num_workers=args.workers)
    print(model)
    evaluator = MultiEvalModel(model, testset.num_class, ctx_list=args.ctx)
    metric = gluoncv.utils.metrics.SegmentationMetric(testset.num_class)
    tbar = tqdm(test_data)
    for (i, (data, dsts)) in enumerate(tbar):
        if args.eval:
            predicts = [pred[0] for pred in evaluator.parallel_forward(data)]
            targets = [target.as_in_context(predicts[0].context) for target in dsts]
            metric.update(targets, predicts)
            (pixAcc, mIoU) = metric.get()
            tbar.set_description(('pixAcc: %.4f, mIoU: %.4f' % (pixAcc, mIoU)))
        else:
            im_paths = dsts
            predicts = evaluator.parallel_forward(data)
            for (predict, impath) in zip(predicts, im_paths):
                predict = (mx.nd.squeeze(mx.nd.argmax(predict[0], 1)).asnumpy() + testset.pred_offset)
                mask = get_color_pallete(predict, args.dataset)
                outname = (os.path.splitext(impath)[0] + '.png')
                mask.save(os.path.join(outdir, outname))