def wait_for_customization(self, vm, poll=10000, sleep=10):
    thispoll = 0
    while (thispoll <= poll):
        eventStarted = self.get_vm_events(['CustomizationStartedEvent'])
        if len(eventStarted):
            thispoll = 0
            while (thispoll <= poll):
                eventsFinishedResult = self.get_vm_events(['CustomizationSucceeded', 'CustomizationFailed'])
                if len(eventsFinishedResult):
                    if (not isinstance(eventsFinishedResult[0], vim.event.CustomizationSucceeded)):
                        self.module.fail_json(msg='Customization failed with error {0}:\n{1}'.format(eventsFinishedResult[0]._wsdlName, eventsFinishedResult[0].fullFormattedMessage))
                        return False
                    break
                else:
                    time.sleep(sleep)
                    thispoll += 1
            return True
        else:
            time.sleep(sleep)
            thispoll += 1
    self.module.fail_json('waiting for customizations timed out.')
    return False