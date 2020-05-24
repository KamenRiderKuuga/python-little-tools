from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.get("http://www.yecaibuluo.com/")

searchBox = browser.find_element_by_id("check-in-email")  #通过id获得文本框
searchBox.send_keys("524472212@qq.com")   #向文本框输入文字
check_in_button = browser.find_element_by_id("check-in-button")  #通过id获得签到按钮
check_in_button.click()
print(browser.page_source)
