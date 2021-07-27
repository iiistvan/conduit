# CON_TC22_Cookie: Adatkezelési nyilatkozat használata
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time


def test_CON_TC22_Cookie():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    def ts():
        time.sleep(3)

    # Step0: Előfeltétel
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

    # Step1: Lapozás az oldal aljára
    driver.find_element_by_tag_name('html').send_keys(Keys.END)
    # js = "window.scrollTo(0, document.body.scrollHeight);"
    # driver.execute_script(js)

    # Step2: Adatvédelmi nyilatkozat elolvasása
    main_window = driver.window_handles[0]
    ts()
    driver.find_element_by_xpath('//div[@id="cookie-policy-panel"]//a').click()
    # print(driver.window_handles)
    new_window = driver.window_handles[1]
    driver.switch_to.window(new_window)
    ts()
    driver.close()
    driver.switch_to.window(main_window)


    # Step3: Adatvédelmi nyilatkozat elfogadása
    driver.find_element_by_xpath('//div[@id="cookie-policy-panel"]//button[2]').click()

    driver.close()
    driver.quit()
