def compare_assume_role_policy_doc(current_policy_doc, new_policy_doc):
    current_policy_doc = json.dumps(current_policy_doc)
    if (current_policy_doc == new_policy_doc):
        return True
    else:
        return False