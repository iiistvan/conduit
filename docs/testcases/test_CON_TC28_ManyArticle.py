# CON_TC28_ManyArticle: Ismételt és sorozatos adatbevitel adatforrásból

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


def test_CON_TC28_ManyArticle():
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
                    return True
        return False

    # Step0: előfeltétel, belépés beépített tesztadattal
    testdata = [['testuser1', 'testuser1@example.com', 'Abcd123$'], ]

    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[0][e + 1])
        ts()
    signin_btn.click()
    ts()

    # Step1: new Article felirat
    newArt_head = driver.find_element_by_xpath('//*[@id="app"]//li[2]/a')
    newArt_head.click()
    ts()

    # Step2: post feltöltése adatokkal csv-ből
    publish_btn = driver.find_element_by_xpath('//form/button')
    with open('ManyDataInput.csv', "r", encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            input_items = driver.find_elements_by_xpath('//form//input')
            for e, i in enumerate(input_items):
                i.send_keys(row[e])
                ts()
            driver.find_element_by_xpath('//form//textarea').send_keys(row[-1])
            publish_btn.click()
            ts()
            assert check_art_item(row[0])
            newArt_head.click()
            ts()
    driver.find_element_by_xpath('//a[@href="#/"]').click()

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
