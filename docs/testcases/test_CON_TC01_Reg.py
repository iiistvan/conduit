# CON_TC01_Reg: Regisztráció
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC01_Reg():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    time.sleep(2)
    # testdata = [['tesztalany1', 'tesztalany1@ta.hu', 'Conduit003'], ['tesztalany12', 'tesztalany12@ta.hu', 'Conduit003'],
    #             ['t360iiistvan1', 't360iiistvan1@gmail.com', 'Conduit003']]
    testdata = ['tesztalany196', 'tesztalany196@ta.hu', 'Conduit003']
    signup_head = driver.find_element_by_xpath('//*[@id="app"]//li[3]/a')

    # try:
    # Step1: Homepage megjelenik
    assert driver.find_element_by_tag_name('h1').text == 'conduit'
    assert driver.find_element_by_xpath('//*[@class="banner"]//p').get_attribute(
        'innerHTML') == 'A place to share your knowledge.'
    print('A vizsgált oldal megjelent.')

    # Step2: elérhető a Sigp Up felirat
    assert driver.find_element_by_xpath('//*[@id="app"]//li[3]').text == 'Sign up'
    print('Elérhető a Sign Up felirat.')

    # Step3: megjelenik a regisztrációs felület
    signup_head.click()
    assert driver.find_element_by_tag_name('h1').text == 'Sign up'
    print('A regisztrációs felület megjelenik.')

    # Step4: látható a username, email, password mező
    ph = ['Username', 'Email', 'Password']
    input_items = driver.find_elements_by_xpath('//form//input')
    for e, i in enumerate(input_items):
        assert i.get_attribute('placeholder') == ph[e]
        print(f"A(z) {ph[e]} beviteli mező megjelenik.")

    # Step5: a tesztadat a regisztráció megtörténik
    signup_btn = driver.find_element_by_xpath('//form/button')
    text_uj = 'Your registration was successful!'
    for e, i in enumerate(input_items):
        i.send_keys(testdata[e])
        time.sleep(1)
    signup_btn.click()
    time.sleep(1)
    assert driver.find_element_by_xpath('//div[@class="swal-text"]').text == text_uj
    print('Sikeres regisztráció!')
    driver.find_element_by_xpath('//div[@class="swal-button-container"]//button').click()
    time.sleep(2)
    assert driver.find_element_by_xpath('//*[@id="app"]//li[4]/a').text == testdata[0]
    print('Felhasználó bejelentkezve, fióknév megjelenik!')

    # Többes regisztráció előkészítése
    # signup_btn = driver.find_element_by_xpath('//form/button')
    # text_uj = 'Your registration was successful!'
    # for _ in range(len(testdata)):
    #     for e, i in enumerate(input_items):
    #         i.send_keys(testdata[_][e])
    #         time.sleep(1)
    #     signup_btn.click()
    #     time.sleep(2)
    #     if driver.find_element_by_xpath('//div[@class="swal-text"]').text == text:
    #         driver.find_element_by_xpath('//div[@class="swal-button-container"]//button').click()
    #         time.sleep(1)
    #         driver.find_element_by_xpath('//*[@id="app"]//li[5]/a').click()
    #         time.sleep(1)
    #         if _ != len(testdata) - 1:
    #             signup_head.click()
    #     else:
    #         driver.find_element_by_xpath('//div[@class="swal-button-container"]//button').click()
    #     time.sleep(2)

    time.sleep(2)

# except:
#     print('Valami nem stimmel!')

# finally:
#     pass
# driver.close()
