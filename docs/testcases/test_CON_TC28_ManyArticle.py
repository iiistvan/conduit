# CON_TC28_ManyArticle: Ismételt és sorozatos adatbevitel adatforrásból
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

def test_CON_TC28_ManyArticle():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # a felvett cikkek meglétének ellenőrzése
    def check_art_item(art_title):
        driver.find_element_by_xpath('//a[@href="#/"]').click()
        time.sleep(1)
        # Oldalszám elemek kigyűjtése
        pages = driver.find_elements_by_class_name('page-link')
        print(len(pages))
        # Oldalon belüli bejegyzések ellenőrzése
        title_list = []
        for i in range(len(pages)):
            pages[i].click()
            time.sleep(2)
            art_input_items = driver.find_elements_by_class_name('article-preview')
            for ai in art_input_items:
                if ai.find_element_by_tag_name('h1').text == art_title:
                    return True
        return False


    # Step0: Előfeltétel, belépés
    testdata = [['testuser1', 'testuser1@example.com', 'Abcd123$'], ]
    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[0][e + 1])
        time.sleep(1)
    signin_btn.click()
    time.sleep(2)

    # Step1: New Article felirat
    newArt_head = driver.find_element_by_xpath('//*[@id="app"]//li[2]/a')
    newArt_head.click()
    time.sleep(2)

    # Step2: Cikk feltöltése adatokkal csv-ből
    input_items = driver.find_elements_by_xpath('//form//input')
    publish_btn = driver.find_element_by_xpath('//form/button')
    # with open('c:\\T360\\PycharmProjects\\selenium-py-peldatar\\selenium2-homework\\ManyDataInput.csv', "r",
    with open('ManyDataInput.csv', "r", encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            input_items = driver.find_elements_by_xpath('//form//input')
            for e, i in enumerate(input_items):
                i.send_keys(row[e])
                time.sleep(1)
            driver.find_element_by_xpath('//form//textarea').send_keys(row[-1])
            publish_btn.click()
            time.sleep(2)
            assert check_art_item(row[0])
            newArt_head.click()
            time.sleep(2)
    driver.find_element_by_xpath('//a[@href="#/"]').click()

    driver.close()
    driver.quit()
