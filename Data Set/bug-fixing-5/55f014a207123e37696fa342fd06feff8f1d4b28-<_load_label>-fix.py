def _load_label(self, idx):
    'Parse xml file and return labels.'
    img_id = self._items[idx]
    anno_path = self._anno_path.format(*img_id)
    root = ET.parse(anno_path).getroot()
    size = root.find('size')
    width = float(size.find('width').text)
    height = float(size.find('height').text)
    if (idx not in self._im_shapes):
        self._im_shapes[idx] = (width, height)
    label = []
    for obj in root.iter('object'):
        try:
            difficult = int(obj.find('difficult').text)
        except ValueError:
            difficult = 0
        cls_name = obj.find('name').text.strip().lower()
        if (cls_name not in self.classes):
            continue
        cls_id = self.index_map[cls_name]
        xml_box = obj.find('bndbox')
        xmin = (float(xml_box.find('xmin').text) - 1)
        ymin = (float(xml_box.find('ymin').text) - 1)
        xmax = (float(xml_box.find('xmax').text) - 1)
        ymax = (float(xml_box.find('ymax').text) - 1)
        try:
            self._validate_label(xmin, ymin, xmax, ymax, width, height)
        except AssertionError as e:
            raise RuntimeError('Invalid label at {}, {}'.format(anno_path, e))
        label.append([xmin, ymin, xmax, ymax, cls_id, difficult])
    return np.array(label)