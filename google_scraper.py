from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re


def is_exist_by_id(driver, _id):
    try:
        driver.find_element_by_id(_id)
    except NoSuchElementException:
        return False
    return True


def get_google_search_results_link(query, filter_keywords="", max_page=3):
    links = []
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/search?q=" + query.replace(" ", "+"))
    repeat_time = 0
    filter_keywords = [keyword.strip() for keyword in filter_keywords.split(',')]
    while True:
        context_element = driver.find_element_by_id("rso")
        elements = context_element.find_elements_by_class_name("g")
        for element in elements:
            element_link = element.find_element_by_tag_name("a").get_attribute("href")
            for keyword in filter_keywords:
                if re.search(r"%s" % re.escape(keyword), element_link.lower()):
                    # print("~~~~~~~~~~~~url '%s' contains keyword '%s'" % (element_link, keyword))
                    links.append(element_link)
                    break
                # print("url '%s'" % element_link)
        repeat_time += 1
        if repeat_time == max_page or not is_exist_by_id(driver, "pnnext"):
            break
        driver.find_element_by_id("pnnext").click()
        WebDriverWait(driver, 20).until(
            lambda browser: browser.execute_script("return document.readyState;") == "complete")
    driver.quit()
    return links


if __name__ == "__main__":
    get_google_search_results_link("pilkada kompas.com 2020", "", 5)
