# CON_TC26_DataModify: Meglévő adat módosítás, felület automatizálás
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC26_DataList():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # Step0: Előfeltétel, belépés beépített tesztadattal
    testdata = ['testuser2', 'testuser2@example.com', 'Abcd123$']
    modified_testdata = ['testuser2', 'testuser2@example.com', 'Abcd123$', 'Short bio about testuser2']
    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')

    for e, i in enumerate(input_items):
        i.send_keys(testdata[e + 1])
    time.sleep(1)
    signin_btn.click()
    time.sleep(2)

    # Step1: Settings felület megnyitása
    settings_head = driver.find_element_by_xpath('//a[@href="#/settings"]')
    settings_head.click()
    time.sleep(2)

    # Step3: Adatok módosítása
    update_btn = driver.find_element_by_xpath('//fieldset/button')
    list_items = driver.find_elements_by_xpath('//fieldset[@class="form-group"]')
    list_settings = []
    time.sleep(2)
    for el, item in enumerate(list_items):
        if el == 2:
            i2 = item.find_element_by_xpath('./*[@placeholder]')
            i2.clear()
            i2.send_keys(modified_testdata[3])
    update_btn.click()
    time.sleep(2)
    text_update = 'Update successful!'
    time.sleep(2)
    assert driver.find_element_by_xpath('//div[@class="swal-title"]').text == text_update
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="swal-button-container"]//button').click()
    time.sleep(2)
    assert modified_testdata[3] == driver.find_element_by_xpath('//fieldset/textarea').get_attribute("value")

    driver.close()
    driver.quit()
