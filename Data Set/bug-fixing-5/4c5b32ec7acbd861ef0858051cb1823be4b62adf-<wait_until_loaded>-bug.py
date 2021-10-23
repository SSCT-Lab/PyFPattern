def wait_until_loaded(self):
    self.browser.wait_until('.entries')
    self.browser.wait_until('[data-test-id="linked-issues"]')
    self.browser.wait_until('[data-test-id="loaded-device-name"]')
    self.browser.wait_until_not('.loading-indicator')