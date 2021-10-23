def reader_creator(image_filename, label_filename, buffer_size):

    def reader():
        if (platform.system() == 'Darwin'):
            zcat_cmd = 'gzcat'
        elif (platform.system() == 'Linux'):
            zcat_cmd = 'zcat'
        else:
            raise NotImplementedError()
        tmp_image_file = tempfile.TemporaryFile(prefix='paddle_dataset')
        m = subprocess.Popen([zcat_cmd, image_filename], stdout=tmp_image_file).communicate()
        tmp_image_file.seek(16)
        tmp_label_file = tempfile.TemporaryFile(prefix='paddle_dataset')
        l = subprocess.Popen([zcat_cmd, label_filename], stdout=tmp_label_file).communicate()
        tmp_label_file.seek(8)
        try:
            while True:
                labels = numpy.fromfile(tmp_label_file, 'ubyte', count=buffer_size).astype('int')
                if (labels.size != buffer_size):
                    break
                images = numpy.fromfile(tmp_image_file, 'ubyte', count=((buffer_size * 28) * 28)).reshape((buffer_size, (28 * 28))).astype('float32')
                images = (((images / 255.0) * 2.0) - 1.0)
                for i in range(buffer_size):
                    (yield (images[i, :], int(labels[i])))
        finally:
            try:
                m.terminate()
            except:
                pass
            try:
                l.terminate()
            except:
                pass
    return reader