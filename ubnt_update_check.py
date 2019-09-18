from selenium import webdriver
import time

driver = webdriver.Chrome()

url = 'https://www.ui.com/download/'
model_name = 'EdgeRouter X SFP'

driver.get(url)
search_box = driver.find_element_by_class_name('downloadSearch__input')
search_box.send_keys(model_name)
search_box.submit()
time.sleep(1)
firmware_table = driver.find_element_by_class_name('downloadResultsRow__details')
firmware_name = firmware_table.find_element_by_class_name('downloadResults__name')

firmware_v = firmware_name.text
latest_firmware = firmware_v.split(':')

print(f'Latest: {latest_firmware[-1]}')
download = input('Do you want to download it? [y/n]: ')

if download.lower() == 'y' or download == '':
    download_firmware = driver.find_element_by_class_name('downloadResults__downloadIcon')
    download_firmware.click()
    time.sleep(1)
    accept_button = driver.find_element_by_class_name('js-eula-agree')
    accept_button.click()
    time.sleep(1)
    download_button = driver.find_element_by_class_name('js-eula-download')
    download_button.click()
    print(f'Downloading {latest_firmware[-1]}')
    time.sleep(12)
    driver.quit()
else:
    driver.quit()
    
driver.quit()
