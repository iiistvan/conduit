# CON_TC02_Logout: Kijelentkezés

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC03_Logout():
    # webdriver konfiguráció, tesztelt oldal megnyitása
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # tesztre vonatkozó egységes, központi időzítés
    def ts():
        time.sleep(3)

    # Step0: előfeltétel, tesztadatok, belépés létező felhasználóval
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

    # Step1: felhasználó bejelentkezve, fióknév megjelenik
    assert driver.find_element_by_xpath('//*[@id="app"]//li[4]/a').text == testdata[0]

    # Step2: elérhető a Logout felirat
    logout_head = driver.find_element_by_xpath('//*[@id="app"]//li[5]/a')
    assert logout_head.text in ' Log out'

    # Step3: kilépési művelet
    logout_head.click()

    # Step4: kilépés után újra elérhető a Sign In felirat, nem elérhető a Your feed
    assert driver.find_element_by_xpath('//a[@href="#/login"]').text == 'Sign in'
    assert driver.find_element_by_xpath('//div[@class="feed-toggle"]//a').text != 'Your Feed'

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
