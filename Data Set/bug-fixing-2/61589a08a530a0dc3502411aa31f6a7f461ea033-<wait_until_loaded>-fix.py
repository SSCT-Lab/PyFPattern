

def wait_until_loaded(self, skip_assistant=None):
    self.browser.wait_until('.entries')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.wait_until('[data-test-id="linked-issues"]')
    self.browser.wait_until('[data-test-id="loaded-device-name"]')
    if (skip_assistant is None):
        self.browser.wait_until('[data-test-id="assistant-cue"]', timeout=6)
