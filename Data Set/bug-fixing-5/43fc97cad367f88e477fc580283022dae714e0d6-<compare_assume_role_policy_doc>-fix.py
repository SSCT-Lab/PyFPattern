def compare_assume_role_policy_doc(current_policy_doc, new_policy_doc):
    if (sort_json_policy_dict(current_policy_doc) == sort_json_policy_dict(json.loads(new_policy_doc))):
        return True
    else:
        return False