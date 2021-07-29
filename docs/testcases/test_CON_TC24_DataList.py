# CON_TC24_DataList: Adatok listázása

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC24_DataList():
    # webdriver konfiguráció, tesztelt oldal megnyitása
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # tesztre vonatkozó egységes, központi időzítés
    def ts():
        time.sleep(3)

    # Step0: Előfeltétel, tesztadatok, belépés létező felhasználóval
    testdata = ['testuser1', 'testuser1@example.com', 'Abcd123$']

    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[e + 1])
    ts()
    signin_btn.click()
    ts()

    # Step1: Settings felület megnyitása
    settings_head = driver.find_element_by_xpath('//a[@href="#/settings"]')
    settings_head.click()
    ts()

    # Step2: Settings felület megnyitása, mezők vizsgálata
    list_items = driver.find_elements_by_xpath('//fieldset[@class="form-group"]')
    list_settings = []
    for el, item in enumerate(list_items):
        list_settings.append(item.find_element_by_xpath('./*[@placeholder]').get_attribute("value"))
    print(list_settings)
    assert testdata[0] == list_settings[1]
    assert testdata[1] == list_settings[3]

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
