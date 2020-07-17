import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# Dumbly finds the first digit to the end of the string.
# Works on most results. [Jul 2020]
def dumb_zip_find(zip):
    for i, char in enumerate(zip):
        if char.isdigit():
            return zip[i:]


# Google Maps base URL
baseURL = 'https://www.google.com/maps/search/'

# Target elements on Google Maps [Jul 2020]
address_search_box = 'searchboxinput'
submit_btn = 'searchbox-searchbutton'

# Selenium options. Included chromedriver only supports Chrome 84.
# You can have it run headless by including: `opts.headless = True`
# Not running in headless for testing [Jul 2020]
opts = Options()
driver = webdriver.Chrome(options=opts, executable_path='./chromedriver')

# Create the output file named zip_codes.csv
writer = csv.writer(open('zip_codes.csv', 'w'))

with open('addresses.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        # Checks that there is enough information to have a useful address
        if len(row) > 4:
            # Since the last three elements in the row list are 'in' 'CITY'
            # 'TX', I am just culling the 'in' and 'TX' and either removing
            # or making them more explicit. row[-2] is the city since it
            # does change throughout the data.
            # Since there are cities/ neighborhoods that are multiple words I
            # should create the city based on the elements between 'in' and 'TX'
            input_address = '+'.join(row[0: -3]) + '+' + row[-2] + '+' + 'TX'

            # Open a new page with the base + search URL and clear inputs
            driver.get(baseURL + input_address)

            # Putting the timeout here as Selenium needs to wait between
            # submission, then server communication, and finally
            # DOM rendering before checking for the resultant zip code
            time.sleep(2)
            try:
                result_container = driver.find_elements_by_class_name('section-result-description')
                if result_container:
                    zip_code = dumb_zip_find(result_container[0].text)

                if not result_container:
                    result_container = driver.find_elements_by_class_name('section-hero-header-title-subtitle')
                    zip_code = dumb_zip_find(result_container[0].text)

                writer.writerow([' '.join(row), zip_code])
            except:
                print(f'Address could not be found: {baseURL + input_address}')

# Just here to gracefully close the webdriver once done.
driver.quit()
