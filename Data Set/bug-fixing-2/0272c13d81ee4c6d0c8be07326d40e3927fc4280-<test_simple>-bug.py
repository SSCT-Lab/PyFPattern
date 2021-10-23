

def test_simple(self):
    self.project.update(first_event=timezone.now())
    self.browser.get(self.path)
    self.browser.wait_until_not('.loading-indicator')
    self.browser.wait_until('.team-list')
    self.browser.snapshot('organization teams list')
    self.browser.click('.team-list a[href]:first-child')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.snapshot('organization team - members list')
    self.browser.click('.nav-tabs li:nth-child(1) a')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.snapshot('organization team - projects list')
    self.browser.click('.nav-tabs li:nth-child(2) a')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.snapshot('organization team - settings')
