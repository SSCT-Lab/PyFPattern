

def _check_load_keypoints(self, coco, entry):
    'Check and load ground-truth keypoints'
    ann_ids = coco.getAnnIds(imgIds=entry['id'], iscrowd=False)
    objs = coco.loadAnns(ann_ids)
    valid_objs = []
    width = entry['width']
    height = entry['height']
    for obj in objs:
        contiguous_cid = self.json_id_to_contiguous[obj['category_id']]
        if (contiguous_cid >= self.num_class):
            continue
        if (max(obj['keypoints']) == 0):
            continue
        (xmin, ymin, xmax, ymax) = bbox_clip_xyxy(bbox_xywh_to_xyxy(obj['bbox']), width, height)
        if ((obj['area'] <= 0) or (xmax <= xmin) or (ymax <= ymin)):
            continue
        joints_3d = np.zeros((self.num_joints, 3, 2), dtype=np.float32)
        for i in range(self.num_joints):
            joints_3d[(i, 0, 0)] = obj['keypoints'][((i * 3) + 0)]
            joints_3d[(i, 1, 0)] = obj['keypoints'][((i * 3) + 1)]
            visible = min(1, obj['keypoints'][((i * 3) + 2)])
            joints_3d[i, :2, 1] = visible
        (center, scale) = self._box_to_center_scale(xmin, ymin, (xmax - xmin), (ymax - ymin))
        valid_objs.append({
            'center': center,
            'scale': scale,
            'joints_3d': joints_3d,
        })
    if (not valid_objs):
        if (not self._skip_empty):
            valid_objs.append({
                'center': np.array([(- 1.0), (- 1.0)]),
                'scale': np.array([0.0, 0.0]),
                'joints_3d': np.zeros((self.num_joints, 3, 2), dtype=np.float32),
            })
    return valid_objs
