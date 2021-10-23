def main():
    if (opt.mode == 'symbolic'):
        data = mx.sym.var('data')
        out = net(data)
        softmax = mx.sym.SoftmaxOutput(out, name='softmax')
        mod = mx.mod.Module(softmax, context=([mx.gpu(i) for i in range(num_gpus)] if (num_gpus > 0) else [mx.cpu()]))
        mod.fit(train_data, eval_data=val_data, num_epoch=opt.epochs, kvstore=opt.kvstore, batch_end_callback=mx.callback.Speedometer(batch_size, max(1, opt.log_interval)), epoch_end_callback=mx.callback.do_checkpoint(('image-classifier-%s' % opt.model)), optimizer='sgd', optimizer_params={
            'learning_rate': opt.lr,
            'wd': opt.wd,
            'momentum': opt.momentum,
        }, initializer=mx.init.Xavier(magnitude=2))
        mod.save_params(('image-classifier-%s-%d-final.params' % (opt.model, epochs)))
    else:
        if (opt.mode == 'hybrid'):
            net.hybridize()
        train(opt.epochs, context)