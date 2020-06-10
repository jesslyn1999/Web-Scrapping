from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


def is_exist_by_id(driver, id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True


def get_google_search_results_link(query, max_page=3):
    links = []
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/search?q=" + query.replace(" ", "+"))
    repeat_time = 0
    while True:
        context_element = driver.find_element_by_id("rso")
        elements = context_element.find_elements_by_class_name('g')
        for element in elements:
            element_link = element.find_element_by_tag_name('a')
            links.append(element_link.get_attribute('href'))
        repeat_time += 1
        if repeat_time == max_page or not is_exist_by_id(driver, 'pnnext'):
            break
        driver.find_element_by_id('pnnext').click()
        WebDriverWait(driver, 20).until(
            lambda browser: browser.execute_script("return document.readyState;") == "complete")
    driver.quit()
    return links


if __name__ == '__main__':
    get_google_search_results_link("pilkada kompas.com 2020", 5)
