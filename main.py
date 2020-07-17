import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Google Maps base URL
baseURL = 'https://www.google.com/maps/search/'

# Target elements on Google Maps [Jul 17, 2020]
address_search_box = 'searchboxinput'
submit_btn = 'searchbox-searchbutton'

# Selenium options. Included chromedriver only supports Chrome 84.
# You can have it run headless by including: `opts.headless = True`
# Not running in headless for testing [Jul 17, 2020]
opts = Options()
driver = webdriver.Chrome(options=opts, executable_path='./chromedriver')

# Create the output file named zip_codes.csv
writer = csv.writer(open('zip_codes.csv', 'w'))

# Here's the meat of the script. It runs through the CSV line by line and
# adds the zip code to the second column of the CSV.
with open('addresses.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in reader:
        if len(row) > 4:
            # Since the last three elements in the row list are 'in' 'CITY'
            # 'TX', I am just culling the 'in' and 'TX' and either removing
            # or making them more explicit.
            input_address = '+'.join(row[0: -3]) + '+' + row[-2] + '+' + 'TX'

            # Open a new page with the base + search URL to clear inputs
            driver.get(baseURL + input_address)

            try:
                # Grab all all of the elements from the DOM that we will be
                # injecting information into.
                # address_elem = driver.find_element_by_id(address_search_box)
                submit_elem = driver.find_element_by_id(submit_btn)

                # Pass information to the address search box
                # address_elem.send_keys(input_address)

                # Finally submit form
                submit = driver.find_element_by_id(submit_btn)
                submit.click()

                # Putting the timeout here as Selenium needs a wait time
                # between submission then server communication and finally
                # DOM rerendering before checking for the resultant zip code
                time.sleep(5)

                # Final grabbing of the resultant zip
                result_container = driver.find_element_by_class_name('section-result-description')
                zip_code = result_container.text
                for i, char in enumerate(zip_code):
                    if char.isdigit():
                        # Grabs from the first found digit to the end of the
                        # content.
                        zip_code = zip_code[i:]
                        break

                writer.writerow([' '.join(row), zip_code])

            except:
                print(f'Address could not be found: {input_address}')

# Just here to gracefully close the webdriver once done.
driver.quit()
