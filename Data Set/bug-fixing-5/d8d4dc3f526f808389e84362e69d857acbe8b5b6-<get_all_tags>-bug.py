def get_all_tags(self):
    '\n        Function to retrieve all tag information\n\n        '
    for tag in self.tag_service.list():
        tag_obj = self.tag_service.get(tag)
        self.global_tags[tag_obj.name] = dict(tag_description=tag_obj.description, tag_used_by=tag_obj.used_by, tag_category_id=tag_obj.category_id, tag_id=tag_obj.id)