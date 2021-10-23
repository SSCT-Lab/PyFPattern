def check_network_policy_diff(self, current_policy, desired_policy):
    '\n        Function to find difference between existing network policy and user given network policy\n        Args:\n            current_policy: Current network policy\n            desired_policy: User defined network policy\n\n        Returns:\n\n        '
    ret = False
    if (current_policy.security.allowPromiscuous != desired_policy.security.allowPromiscuous):
        ret = True
    if (current_policy.security.forgedTransmits != desired_policy.security.forgedTransmits):
        ret = True
    if (current_policy.security.macChanges != desired_policy.security.macChanges):
        ret = True
    return ret