

def _read_img(self, img_name, label_name):
    img = Image.open(os.path.join(self.root_dir, img_name))
    label = Image.open(os.path.join(self.root_dir, label_name))
    assert (img.size == label.size)
    img = np.array(img, dtype=np.float32)
    label = np.array(label)
    if (self.cut_off_size is not None):
        max_hw = max(img.shape[0], img.shape[1])
        min_hw = min(img.shape[0], img.shape[1])
        if (min_hw > self.cut_off_size):
            rand_start_max = int(np.random.uniform(0, ((max_hw - self.cut_off_size) - 1)))
            rand_start_min = int(np.random.uniform(0, ((min_hw - self.cut_off_size) - 1)))
            if (img.shape[0] == max_hw):
                img = img[rand_start_max:(rand_start_max + self.cut_off_size), rand_start_min:(rand_start_min + self.cut_off_size)]
                label = label[rand_start_max:(rand_start_max + self.cut_off_size), rand_start_min:(rand_start_min + self.cut_off_size)]
            else:
                img = img[rand_start_min:(rand_start_min + self.cut_off_size), rand_start_max:(rand_start_max + self.cut_off_size)]
                label = label[rand_start_min:(rand_start_min + self.cut_off_size), rand_start_max:(rand_start_max + self.cut_off_size)]
        elif (max_hw > self.cut_off_size):
            rand_start = int(np.random.uniform(0, ((max_hw - min_hw) - 1)))
            if (img.shape[0] == max_hw):
                img = img[rand_start:(rand_start + min_hw), :]
                label = label[rand_start:(rand_start + min_hw), :]
            else:
                img = img[:, rand_start:(rand_start + min_hw)]
                label = label[:, rand_start:(rand_start + min_hw)]
    reshaped_mean = self.mean.reshape(1, 1, 3)
    img = (img - reshaped_mean)
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 1, 2)
    img = np.expand_dims(img, axis=0)
    label = np.array(label)
    label = np.expand_dims(label, axis=0)
    return (img, label)
