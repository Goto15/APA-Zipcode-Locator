import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# Dumbly finds the first digit in the string 'City, State Zip' to the end of the
# string. Works for most results. [Jul 2020]
def dumb_zip_find(zip):
    for i, char in enumerate(zip):
        if char.isdigit():
            return zip[i:]


# Google Maps search base URL
baseURL = 'https://www.google.com/maps/search/'

# Selenium options. Included chromedriver only supports Chrome 84.
# You can have it run headless by including: `opts.headless = True`
# [Jul 2020]
opts = Options()
opts.headless = True
driver = webdriver.Chrome(options=opts, executable_path='./chromedriver')

# Create output file
writer = csv.writer(open('zip_codes.csv', 'w'))

with open('addresses.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        # Checks that there is enough information to have a useful address
        if len(row) > 4:
            # Since the last three elements in the row list are 'in' 'CITY' 'TX',
            # I am just culling the 'in' and 'TX' and either removing or making
            # them more explicit. row[-2] is the city since it does change
            # throughout the data.
            # TODO: Handle multi-word cities / neighborhoods
            input_address = '+'.join(row[0: -3]) + '+' + row[-2] + '+' + 'TX'

            # Constructs the Google Maps search URL to bypass a few Selenium inputs
            driver.get(baseURL + input_address)

            # Putting the timeout here as Selenium needs to wait between submission,
            # then server communication, and finally DOM rendering before checking
            # for the resultant zip code. Also don't want to get banned from G Maps
            time.sleep(2)
            try:
                # Checks for Google guesstimate results.
                result_container = driver.find_elements_by_class_name('section-result-description')
                if result_container:
                    zip_code = dumb_zip_find(result_container[0].text)

                # Checks for specific address results.
                if not result_container:
                    result_container = driver.find_elements_by_class_name('section-hero-header-title-subtitle')
                    zip_code = dumb_zip_find(result_container[0].text)

                # TODO: Check for array of likely results. Currently unimplemented
                # if not result_container[0].text:
                #     # Need to find the first result and click on it.
                #     # After that find the first result named ugiz4pqJLAG__primary-text gm2-body-2 and pull the text.
                #     closest_result = driver.find_elements_by_class_name('section-result')[0]
                #     closest_result.click()
                #     time.sleep(1)

                writer.writerow([' '.join(row), zip_code])
            except:
                # If we can't parse a zip save the address and the URL for human
                # troubleshooting.
                writer.writerow([input_address, baseURL + input_address])

driver.quit()
