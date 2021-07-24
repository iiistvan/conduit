# CON_TC02_Logout: Kilépés vizsgálata
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC03_Logout():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # Step0: Előfeltétel
    testdata = ['tesztalany1', 'tesztalany1@ta.hu', 'Conduit003']
    signin_head = driver.find_element_by_xpath('//a[@href="#/login"]')
    signin_head.click()
    input_items = driver.find_elements_by_xpath('//form//input')
    signin_btn = driver.find_element_by_xpath('//form/button')

    for e, i in enumerate(input_items):
        i.send_keys(testdata[e + 1])
        time.sleep(1)
    signin_btn.click()
    time.sleep(2)

    # Step1: Felhasználó bejelentkezve
    assert driver.find_element_by_xpath('//*[@id="app"]//li[4]/a').text == testdata[0]
    # print('Felhasználó bejelentkezve, fióknév megjelenik!')

    # Step2: elérhető a Logout felirat
    logout_head = driver.find_element_by_xpath('//*[@id="app"]//li[5]/a')
    assert logout_head.text in ' Log out'

    # Step3: Kilépési művelet
    logout_head.click()

    # Step4: elérhető a Sign In felirat
    assert driver.find_element_by_xpath('//a[@href="#/login"]').text == 'Sign in'
    # print('Kilépés után újra elérhető a Sign In felirat.')
    assert driver.find_element_by_xpath('//div[@class="feed-toggle"]//a').text != 'Your Feed'
    # print('Nem elérhető a Your feed.')

    driver.close()
    driver.quit()
