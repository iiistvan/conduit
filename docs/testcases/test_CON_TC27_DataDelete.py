# CON_TC27_DataDelete: Adat vagy adatok törlése

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC27_DataDelete():
    # webdriver konfiguráció, tesztelt oldal megnyitása
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # tesztre vonatkozó egységes, központi időzítés
    def ts():
        time.sleep(3)

    # a felvett cikkek meglétének ellenőrzése
    def check_art_item(art_title):
        driver.find_element_by_xpath('//a[@href="#/"]').click()
        ts()
        # Oldalszám elemek kigyűjtése
        pages = driver.find_elements_by_class_name('page-link')
        print(len(pages))
        # Oldalon belüli bejegyzések ellenőrzése
        title_list = []
        for i in range(len(pages)):
            pages[i].click()
            ts()
            art_input_items = driver.find_elements_by_class_name('article-preview')
            for ai in art_input_items:
                if ai.find_element_by_tag_name('h1').text == art_title:
                    return ai
        return ''

    # az átadott elem törlése
    def del_item(del_item):
        del_item.click()
        ts()
        del_art_btn = driver.find_element_by_xpath('//span/button')
        ts()
        del_art_btn.click()
        ts()

    # Step0: Előfeltétel, belépés beépített tesztadattal
    testdata = ['testuser2', 'testuser2@example.com', 'Abcd123$']
    new_article = ['TorlendoCim', 'Tema', 'Tag']
    new_art_szoveg = ['07272 Ez egy új bejegyzés a vizsgamunkába, ezt fogom törölni később.']

    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[e + 1])
    ts()
    signin_btn.click()
    ts()

    home_head = driver.find_element_by_xpath('//*[@id="app"]//li[1]/a')
    newArt_head = driver.find_element_by_xpath('//*[@id="app"]//li[2]/a')
    newArt_head.click()
    ts()

    # Step1: törlendő cikk létrehozása
    publish_btn = driver.find_element_by_xpath('//form/button')
    input_items = driver.find_elements_by_xpath('//form//input')
    for e, i in enumerate(input_items):
        i.send_keys(new_article[e])
        ts()
    driver.find_element_by_xpath('//form//textarea').send_keys(new_art_szoveg)
    publish_btn.click()
    ts()
    home_head.click()
    ts()

    # Step2: létrehozott cikk keresése, majd törlése
    del_item(check_art_item(new_article[0]))
    ts()

    # Step3: törlés ellenőrzése
    assert check_art_item(new_article[0]) == ''

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
