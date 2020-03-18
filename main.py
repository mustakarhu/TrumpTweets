from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

# micro sleep for the site to load, sleep for the dataset to load
u_sleep = 2
sleep = 5

if __name__ == '__main__':

    # url of the site where we want to fetch the data
    url = 'http://www.trumptwitterarchive.com/archive'
    periods = [['01', 'Jan', Keys.ARROW_RIGHT, '2020'],
               ['18', 'Mar', Keys.ARROW_RIGHT, '2020']]
    options = ['2']
    export_option = '3'  # '3' for csv '4' for json

    # set-up chrome webdriver
    web_options = webdriver.ChromeOptions()
    web_options.add_argument('incognito')
    # options.add_argument('headless')
    browser = webdriver.Chrome(options=web_options)
    browser.get(url)

    time.sleep(sleep)
    # set the start and end periods
    for d in range(2):
        dates = browser.find_element_by_xpath(f'//*[@id="control-dates"]/input[{d+1}]')
        for elem in periods[d]:
            dates.send_keys(elem)
            time.sleep(u_sleep)

    # open options menu
    options_button = browser.find_element_by_xpath('//*[@id="options-button"]/button')
    options_button.click()
    for elem in options:
        opt = browser.find_element_by_xpath(f'//*[@id="options-button"]/ul/li[{elem}]/input')
        opt.click()

    # open export menu
    export_button = browser.find_element_by_xpath('//*[@id="exports-button"]/button')
    export_button.click()
    export_format_button = browser.find_element_by_xpath(f'//*[@id="exports-button"]/ul/li[{export_option}]')
    export_format_button.click()
    # need to wait info to load
    time.sleep(sleep)
    refresh = browser.find_element_by_xpath('//*[@id="export-box"]/div[2]/button[1]').click()
    time.sleep(sleep)

    content = browser.find_element_by_xpath('//*[@id="export-box"]/textarea').get_attribute('value')

    t = (content.split('\n'))

    with open('tweets.csv', 'w', encoding='utf-8') as f:
        for entry in t:
            f.write(f'{entry}\n')