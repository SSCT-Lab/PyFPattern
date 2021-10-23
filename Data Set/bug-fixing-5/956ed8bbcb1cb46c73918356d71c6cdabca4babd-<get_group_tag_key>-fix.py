def get_group_tag_key(self, project_id, group_id, environment_id, key):
    return self.__get_tag_key_and_top_values(project_id, group_id, environment_id, key, limit=9)