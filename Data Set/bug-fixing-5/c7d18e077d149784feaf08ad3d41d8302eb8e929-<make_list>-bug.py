def make_list(args):
    image_list = list_image(args.root, args.recursive, args.exts)
    image_list = list(image_list)
    if (args.shuffle is True):
        random.seed(100)
        random.shuffle(image_list)
    N = len(image_list)
    chunk_size = (((N + args.chunks) - 1) / args.chunks)
    for i in xrange(args.chunks):
        chunk = image_list[(i * chunk_size):((i + 1) * chunk_size)]
        if (args.chunks > 1):
            str_chunk = ('_%d' % i)
        else:
            str_chunk = ''
        sep = int((chunk_size * args.train_ratio))
        sep_test = int((chunk_size * args.test_ratio))
        if (args.train_ratio == 1.0):
            write_list(((args.prefix + str_chunk) + '.lst'), chunk)
        else:
            if args.test_ratio:
                write_list(((args.prefix + str_chunk) + '_test.lst'), chunk[:sep_test])
            if ((args.train_ratio + args.test_ratio) < 1.0):
                write_list(((args.prefix + str_chunk) + '_val.lst'), chunk[(sep_test + sep):])
            write_list(((args.prefix + str_chunk) + '_train.lst'), chunk[sep_test:(sep_test + sep)])