from selenium import webdriver
from selenium.webdriver.common.by import By


def zhihuHot():
    browser = webdriver.Chrome("chromedriver.exe")
    browser.get('http://www.zhihu.com/billboard')
    browser.implicitly_wait(10)
    x = browser.find_elements(by=By.CLASS_NAME, value="HotList-itemBody")
    results = []
    for item in x:
        results.append(item.text)
    browser.close()
    return results
