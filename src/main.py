import time
import queue
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service


def initialize_selenium():
    options = webdriver.FirefoxOptions()
    # options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (
    # KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    s = Service("webdrivers/geckodriver-v0.32.2-win32/geckodriver.exe")
    driver = webdriver
    try:
        driver = webdriver.Firefox(
            service=s,
            options=options
        )
    except Exception as ex:
        print(ex)
        return webdriver
    finally:
        return driver
        pass


def get_first_level(driver, url):
    try:
        driver.get(url=url)
        time.sleep(5)

        with open("index_selenium.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        pass

    with open("index_selenium.html", "r", encoding="utf-8") as file:
        src = file.read()

    # get hotels urls
    soup = BeautifulSoup(src, "lxml")

    subcategory_with_childs = soup.find_all("div", class_="subcategory__item subcategory__item_with-childs")
    subcategory_list = list()
    for subcategory_url in subcategory_with_childs:
        subcategory_list.append("https://www.dns-shop.ru" + subcategory_url.find("a").get("href"))
    [print(i) for i in subcategory_list]
    return subcategory_list


def main():
    subcategory_list = queue.Queue()
    subcategory_list.put("https://www.dns-shop.ru/catalog/")
    driver = initialize_selenium()
    while not subcategory_list.empty():
        link = subcategory_list.get()
        link_list = get_first_level(driver, link)
        [subcategory_list.put(i) for i in link_list]


if __name__ == '__main__':
    main()
