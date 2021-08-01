# CON_TC02_Login: Bejelentkezés
# létező, korábban regisztrált felhasználóval

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC02_Login():
    # webdriver konfiguráció, tesztelt oldal megnyitása
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # tesztre vonatkozó egységes, központi időzítés
    def ts():
        time.sleep(5)

    # Step0: előfeltétel, tesztadatok
    testdata = ['testuser1', 'testuser1@example.com', 'Abcd123$']

    # homepage megjelenik
    assert driver.find_element_by_tag_name('h1').text == 'conduit'
    assert driver.find_element_by_xpath('//*[@class="banner"]//p').get_attribute(
        'innerHTML') == 'A place to share your knowledge.'

    # Step1: elérhető a Sign In felirat
    assert driver.find_element_by_xpath('//a[@href="#/login"]').text == 'Sign in'

    # Step2: megjelenik a regisztrációs felület, látható az email, password mező
    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    assert driver.find_element_by_tag_name('h1').text == 'Sign in'
    # print('A bejelentkező felület megjelenik.')
    ph = ['Email', 'Password']
    input_items = driver.find_elements_by_xpath('//form//input')
    for e, i in enumerate(input_items):
        assert i.get_attribute('placeholder') == ph[e]
        # print(f"A(z) {ph[e]} beviteli mező megjelenik.")

    # Step3: belépés a tesztadattal
    signin_btn = driver.find_element_by_xpath('//form/button')
    for e, i in enumerate(input_items):
        i.send_keys(testdata[e + 1])
        ts()
    signin_btn.click()
    ts()

    # Step4: felhasználó bejelentkezve, fióknév megjelenik
    assert driver.find_element_by_xpath('//*[@id="app"]//li[4]/a').text == testdata[0]

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
