# CON_TC23_Pages: Több oldalas lista bejárása
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time


def test_CON_TC23_Pages():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    def ts():
        time.sleep(3)

    # Step0: Előfeltétel
    testdata = ['tesztalany1', 'tesztalany1@ta.hu', 'Conduit003']
    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[e + 1])
        ts()
    signin_btn.click()
    ts()

    # Step1: Oldalszám elemek kigyűjtése
    pages = driver.find_elements_by_class_name('page-link')

    # Step2: Oldalon belüli bejegyzések ellenőrzése
    for i in range(len(pages)):
        pages[i].click()
        ts()
        articles = driver.find_elements_by_xpath('//div[@class="article-preview"]')
        print(f"{i + 1}.oldal bejegyzéseinek száma {len(articles)}")

    driver.close()
    driver.quit()
