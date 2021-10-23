@pytest.fixture(scope='function')
def browser(request, percy, live_server):
    window_size = request.config.getoption('window_size')
    (window_width, window_height) = list(map(int, window_size.split('x', 1)))
    driver_type = request.config.getoption('selenium_driver')
    headless = (not request.config.getoption('no_headless'))
    if (driver_type == 'chrome'):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('w3c', False)
        options.add_argument('no-sandbox')
        options.add_argument('disable-gpu')
        options.add_argument('window-size={}'.format(window_size))
        if headless:
            options.add_argument('headless')
        chrome_path = request.config.getoption('chrome_path')
        if chrome_path:
            options.binary_location = chrome_path
        chromedriver_path = request.config.getoption('chromedriver_path')
        if chromedriver_path:
            driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
        else:
            driver = webdriver.Chrome(chrome_options=options)
    elif (driver_type == 'firefox'):
        driver = webdriver.Firefox()
    elif (driver_type == 'phantomjs'):
        phantomjs_path = request.config.getoption('phantomjs_path')
        if (not phantomjs_path):
            phantomjs_path = os.path.join('node_modules', 'phantomjs-prebuilt', 'bin', 'phantomjs')
        driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    else:
        raise pytest.UsageError('--driver must be specified')
    driver.set_window_size(window_width, window_height)

    def fin():
        try:
            driver.quit()
        except Exception:
            pass
    request.node._driver = driver
    request.addfinalizer(fin)
    browser = Browser(driver, live_server, percy)
    if hasattr(request, 'cls'):
        request.cls.browser = browser
    request.node.browser = browser
    percy.loader.webdriver = driver
    return driver