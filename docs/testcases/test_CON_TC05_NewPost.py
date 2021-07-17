# CON_TC05_NewPost: Új adat bevitel
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time


def test_CON_TC05_NewPost():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # Step0: Előfeltétel
    testdata = [['tesztalany1', 'tesztalany1@ta.hu', 'Conduit003'], ['tesztalany2', 'tesztalany2@ta.hu', 'Conduit003']]
    new_article = ['CikkCim', 'Tema', 'Tag']
    new_art_szoveg = ['Ez egy új bejegyzés a vizsgamunkába.']

    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[0][e + 1])
        time.sleep(1)
    signin_btn.click()
    time.sleep(2)

    # Step4: elérhető a New Article felirat
    newArt_head = driver.find_element_by_xpath('//*[@id="app"]//li[2]/a')
    assert newArt_head.text in ' New Article'

    # Step5: elérhető a New Article felirat
    newArt_head.click()
    time.sleep(2)
    ph_i = ["Article Title", "What's this article about?", "Enter tags"]
    ph_t = ["Write your article (in markdown)"]
    input_items = driver.find_elements_by_xpath('//form//input')
    # print(len(ph_i), len(input_items))
    for e, i in enumerate(input_items):
        assert i.get_attribute('placeholder') == ph_i[e]
        print(f"A(z) {ph_i[e]} beviteli mező megjelenik.")
    assert driver.find_element_by_xpath('//form//textarea').get_attribute('placeholder') == ph_t[0]
    print(f"A(z) {ph_t[0]} beviteli mező megjelenik.")

    # Step6: Cikk feltöltése adatokkal
    publish_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(new_article[e])
        time.sleep(1)
    driver.find_element_by_xpath('//form//textarea').send_keys(new_art_szoveg)
    publish_btn.click()
    time.sleep(2)

    # Step7: a felületen a title, a szerző, tag,  Edit és Delete gomb, valamint egy üres comment ablak és Post Comment gomb
    assert driver.find_element_by_xpath('//div[@class="banner"]//h1').text == new_article[0]
    assert driver.find_element_by_xpath('//div[@class="info"]/a').text == testdata[0][0]
    assert driver.find_element_by_xpath('//div[@class="tag-list"]/a').text == new_article[2]
    assert driver.find_element_by_xpath('//a[@href="#/editor/cikkcim"]/span').text == ' Edit Article'
    assert driver.find_element_by_xpath('//button/span').text == ' Delete Article'
    assert driver.find_element_by_xpath('//form/div/textarea[@placeholder="Write a comment..."]')
    assert driver.find_element_by_xpath('//form/div/button').text == 'Post Comment'
