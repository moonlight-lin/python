# -*- coding:utf-8 -*-
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


URL_MAP = {
    "20200416":
    "https://b2c.csair.com/ita/intl/zh/flights?flex=1&m=0&p=100&t=LHR-CAN-20200416|LON&egs=ITA,ITA&open=1&flex=1&nb=1",

    "20200423":
    "https://b2c.csair.com/ita/intl/zh/flights?flex=1&m=0&p=100&t=LHR-CAN-20200423|LON&egs=ITA,ITA&open=1&flex=1&nb=1"
}

URL_DEBUG_MAP = {
    "20200910":
    "https://b2c.csair.com/ita/intl/zh/flights?flex=1&m=0&p=100&t=LHR-CAN-20200910|LON&egs=ITA,ITA&open=1&flex=1&nb=1"
}


DEBUG = True


def log(msg):
    if DEBUG:
        print("[" + str(datetime.now()) + "] " + msg)


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')      ## no GUI
    chrome_options.add_argument('--disable-gpu')

    # need to download chromedriver from chrome official web page
    driver = webdriver.Chrome(executable_path=r'chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)

    driver.implicitly_wait(20)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)

    log("get_driver finished")

    return driver


# noinspection PyBroadException
def parse_url(url_map):
    for date in url_map:
        driver = get_driver()

        url = url_map[date]
        log("date : " + str(date))
        log("url : " + str(url))
        driver.get(url)
        log("get url finished, sleep 5 seconds")
        time.sleep(5)
        log("wake up")

        # driver.save_screenshot('./csair.png')

        try:
            ticket_list_element = driver.find_element_by_class_name('sh-list-view')
            log("get sh-list-view successfully")
        except Exception, e:
            # suppose it always exist
            log("failed to get sh-list-view")
            driver.close()
            driver.quit()
            continue

        try:
            ticket_items = ticket_list_element.find_elements_by_class_name('item')
            log("get item successfully")
        except Exception, e:
            # no ticket
            log("no ticket")
            driver.close()
            driver.quit()
            continue

        found = False
        for ticket_item in ticket_items:
            try:
                ticket_item.find_element_by_class_name('sold-out')
                log("sold-out")
            except Exception, e:
                try:
                    price = ticket_item.find_element_by_class_name('sh-prc-fare').text()
                    log(price)
                    found = True
                    break
                except Exception, e:
                    log("failed to get price : " + str(e))
                    continue

        if found:
            log("has ticket")

        '''
        if DEBUG:
            # only print the source, not the HTML
            print driver.page_source
        '''

        driver.close()
        driver.quit()


def main():
    parse_url(URL_MAP)
    parse_url(URL_DEBUG_MAP)


if __name__ =="__main__":
    main()
