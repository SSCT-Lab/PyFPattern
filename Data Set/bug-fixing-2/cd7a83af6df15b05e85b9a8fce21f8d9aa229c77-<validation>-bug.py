

def validation(self, epoch):
    self.metric.reset()
    tbar = tqdm(self.eval_data)
    for (i, (data, target)) in enumerate(tbar):
        outputs = self.evaluator(data.astype(args.dtype, copy=False))
        outputs = [x[0] for x in outputs]
        targets = mx.gluon.utils.split_and_load(target, args.ctx)
        self.metric.update(targets, outputs)
        (pixAcc, mIoU) = self.metric.get()
        tbar.set_description(('Epoch %d, validation pixAcc: %.3f, mIoU: %.3f' % (epoch, pixAcc, mIoU)))
        mx.nd.waitall()
