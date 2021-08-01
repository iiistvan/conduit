# CON_TC05_NewPost: Új adat bevitel

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC05_NewPost():
    # webdriver konfiguráció, tesztelt oldal megnyitása
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # tesztre vonatkozó egységes, központi időzítés
    def ts():
        time.sleep(3)

    # Step0: előfeltétel, tesztadatok, belépés létező felhasználóval
    testdata = [['testuser1', 'testuser1@example.com', 'Abcd123$'], ['testuser2', 'testuser2@example.com', 'Abcd123$']]
    new_article = ['CikkCim', 'Tema', 'Tag']
    new_art_szoveg = ['Ez egy új bejegyzés a vizsgamunkába.']

    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[0][e + 1])
        ts()
    signin_btn.click()
    ts()

    # Step1: elérhető a New Article felirat
    newArt_head = driver.find_element_by_xpath('//*[@id="app"]//li[2]/a')
    assert newArt_head.text in ' New Article'

    # Step2: post mezők ellenőrzése
    newArt_head.click()
    ts()
    ph_i = ["Article Title", "What's this article about?", "Enter tags"]
    ph_t = ["Write your article (in markdown)"]
    input_items = driver.find_elements_by_xpath('//form//input')
    # print(len(ph_i), len(input_items))
    for e, i in enumerate(input_items):
        assert i.get_attribute('placeholder') == ph_i[e]
        # print(f"A(z) {ph_i[e]} beviteli mező megjelenik.")
    assert driver.find_element_by_xpath('//form//textarea').get_attribute('placeholder') == ph_t[0]
    # print(f"A(z) {ph_t[0]} beviteli mező megjelenik.")

    # Step2: post feltöltése adatokkal
    publish_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(new_article[e])
        ts()
    driver.find_element_by_xpath('//form//textarea').send_keys(new_art_szoveg)
    publish_btn.click()
    ts()

    # Step3: a felületen a kitöltésnek megfelelően megjelenik a title, a szerző, tag,  Edit és Delete gomb,
    # valamint egy üres comment ablak és Post Comment gomb
    assert driver.find_element_by_xpath('//div[@class="banner"]//h1').text == new_article[0]
    assert driver.find_element_by_xpath('//div[@class="info"]/a').text == testdata[0][0]
    assert driver.find_element_by_xpath('//div[@class="tag-list"]/a').text == new_article[2]
    assert driver.find_element_by_xpath('//a[@href="#/editor/cikkcim"]/span').text == ' Edit Article'
    assert driver.find_element_by_xpath('//button/span').text == ' Delete Article'
    assert driver.find_element_by_xpath('//form/div/textarea[@placeholder="Write a comment..."]')
    assert driver.find_element_by_xpath('//form/div/button').text == 'Post Comment'

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
