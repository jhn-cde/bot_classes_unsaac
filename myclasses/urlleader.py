from selenium import webdriver

class UrlLeader():
    def __init__(self, cur_dir):
        self.cur_dir = cur_dir
        # create a headless browser
        self.option = webdriver.ChromeOptions()
        self.option.binary_location = '/usr/bin/brave-browser-nightly'
        self.option.add_argument("--start-maximized")
        #self.option.add_argument("use-fake-device-for-media-stream")
        self.option.add_argument("use-fake-ui-for-media-stream")
        self.pageurl = ''
        self.browser = None
        self.element = None

    def open_browser(self):
        self.browser = webdriver.Chrome(executable_path=self.cur_dir + '/driver/chromedriver', options = self.option)
    
    def open_url(self, url):
        self.pageurl = url
        self.browser.get(self.pageurl)
    def new_window(self):
        self.browser.execute_script("window.open()")
        new_window = self.browser.window_handles[1]
        self.browser.switch_to_window(new_window)

    def close_browser(self):
        self.browser.close()

    def find_element_by_id(self, id):
        self.element = self.browser.find_element_by_id(id)
    def find_element_by_class(self, class_name):
        self.element = self.browser.find_element_by_class_name(class_name)

    def find_element_by_xpath(self, xpath):
        self.element = self.browser.find_element_by_xpath(xpath)
    def find_childs_by_xpath(self, xpath):
        return self.element.find_elements_by_xpath(xpath)

def test():
    python_website = UrlLeader()
    python_website.open_url('https://www.python.org/')
    python_website.close_browser()
    return True

if __name__ == '__main__':
    test()
