# CON_TC25_DataBackup: Adatok lementése felületről

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


def test_CON_TC25_DataBackup():
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

    # Step1: Popular tags kigyűjtése, fájlba kiíratás
    pop_tags = driver.find_elements_by_xpath('//div[@class="sidebar"]/div/a')
    with open('./docs/testcases/PopTagsExport.csv', "w", encoding='utf-8') as csvfile:
        # with open('c:\\T360\\PycharmProjects\\selenium-py-peldatar\\selenium2-homework\\PopTagsExport.csv', "w",
        #           encoding='utf-8') as csvfile:
        csvfile.write(f'Tag_name,Tag_href\n')
        for pt in pop_tags:
            csvfile.write(f'{pt.text},{pt.get_attribute("href")}\n')
            # print(f'{pt.text},{pt.get_attribute("href")}')
    ts()

    # Step2: Popular tags kigyűjtése, fájlból olvasás ellenőrzés
    with open('./docs/testcases/PopTagsExport.csv', "r", encoding='utf-8') as csvfile2:
        csvreader = csv.reader(csvfile2, delimiter=',')
        next(csvreader)
        for e, row in enumerate(csvreader):
            pt = pop_tags[e]
            assert row[0] == pt.text
            assert row[1] == pt.get_attribute("href")

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
