def get_data_loader(data_dir, batch_size, num_workers):
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    jitter_param = 0.4
    lighting_param = 0.1

    def batch_fn(batch, ctx):
        data = gluon.utils.split_and_load(batch[0], ctx_list=ctx, batch_axis=0)
        label = gluon.utils.split_and_load(batch[1], ctx_list=ctx, batch_axis=0)
        return (data, label)
    transform_train = transforms.Compose([transforms.RandomResizedCrop(224), transforms.RandomFlipLeftRight(), transforms.RandomColorJitter(brightness=jitter_param, contrast=jitter_param, saturation=jitter_param), transforms.RandomLighting(lighting_param), transforms.ToTensor(), normalize])
    transform_test = transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), normalize])
    train_data = gluon.data.DataLoader(imagenet.classification.ImageNet(data_dir, train=True).transform_first(transform_train), batch_size=batch_size, shuffle=True, last_batch='discard', num_workers=num_workers)
    val_data = gluon.data.DataLoader(imagenet.classification.ImageNet(data_dir, train=False).transform_first(transform_test), batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return (train_data, val_data, batch_fn)