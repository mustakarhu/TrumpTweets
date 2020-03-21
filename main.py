from selenium import webdriver  # to scrape the data
from selenium.webdriver.common.keys import Keys  # input keys for commands
import time  # used for waiting periods
import datetime

# micro sleep for the site to load, sleep for the dataset to load
u_sleep = 0.5
sleep = 1
PRINT = True

if __name__ == '__main__':

    # url of the site where we want to fetch the data
    url = 'http://www.trumptwitterarchive.com/archive'
    # set the periods to which we will gather our data. This is a
    # list of commands for the selenium date picker
    today = datetime.date.today()
    day = str(today.strftime('%d'))
    month = str(today.strftime('%b'))
    year = str(today.strftime('%Y'))

    periods = [['01', 'Jan', Keys.ARROW_RIGHT, '2016'],
               [day, month, Keys.ARROW_RIGHT, year]]

    options = []
    export_option = '3'  # '3' for csv '4' for json

    # set-up chrome webdriver
    # select the options here
    if PRINT:
        print('Setting up web scraper')
    web_options = webdriver.ChromeOptions()
    web_options.add_argument('incognito')
    web_options.add_argument('headless')
    web_options.add_argument('disable-gpu')
    web_options.add_argument('window-size=1920,1080')
    browser = webdriver.Chrome(options=web_options)
    if PRINT:
        print('retrieving website data')
    browser.get(url)

    time.sleep(sleep)
    # set the start and end periods
    if PRINT:
        print('Setting up filter parameters')
    for d in range(2):
        dates = browser.find_element_by_xpath(f'//*[@id="control-dates"]/input[{d+1}]')
        for elem in periods[d]:
            dates.send_keys(elem)
            time.sleep(u_sleep)

    # open options menu and select the options from the variable options defined above
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
    # need to wait info to load especially for large datasets
    time.sleep(sleep)
    if PRINT:
        print('collecting data')

    # refresh if not loaded
    # refresh = browser.find_element_by_xpath('//*[@id="export-box"]/div[2]/button[1]').click()
    # time.sleep(sleep)
    content = browser.find_element_by_xpath('//*[@id="export-box"]/textarea').get_attribute('value')
    # close the browser
    browser.close()

    if PRINT:
        print('write on file')

    # breaking the  content into entries with split and save with utf8 encoding.
    t = content.split('\n')
    with open('tweets.csv', 'w', encoding='utf-8') as f:
        for entry in t:
            f.write(f'{entry}\n')
