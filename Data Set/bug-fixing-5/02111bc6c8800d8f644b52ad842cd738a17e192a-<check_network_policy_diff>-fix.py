@staticmethod
def check_network_policy_diff(current_policy, desired_policy):
    '\n        Function to find difference between existing network policy and user given network policy\n        Args:\n            current_policy: Current network policy\n            desired_policy: User defined network policy\n\n        Returns: True if difference found, False if not.\n\n        '
    ret = False
    if ((current_policy.security.allowPromiscuous != desired_policy.security.allowPromiscuous) or (current_policy.security.forgedTransmits != desired_policy.security.forgedTransmits) or (current_policy.security.macChanges != desired_policy.security.macChanges)):
        ret = True
    return ret