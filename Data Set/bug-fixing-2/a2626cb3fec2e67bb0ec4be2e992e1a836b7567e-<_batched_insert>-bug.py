

def _batched_insert(self, objs, fields, batch_size):
    '\n        A helper method for bulk_create() to insert the bulk one batch at a\n        time. Insert recursively a batch from the front of the bulk and then\n        _batched_insert() the remaining objects again.\n        '
    if (not objs):
        return
    ops = connections[self.db].ops
    batch_size = (batch_size or max(ops.bulk_batch_size(fields, objs), 1))
    inserted_ids = []
    for item in [objs[i:(i + batch_size)] for i in range(0, len(objs), batch_size)]:
        if connections[self.db].features.can_return_ids_from_bulk_insert:
            inserted_id = self._insert(item, fields=fields, using=self.db, return_id=True)
            if isinstance(inserted_id, list):
                inserted_ids.extend(inserted_id)
            else:
                inserted_ids.append(inserted_id)
        else:
            self._insert(item, fields=fields, using=self.db)
    return inserted_ids
