# CON_TC25_DataBackup: Adatok lementése felületről
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_CON_TC25_DataBackup():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")


    # időzités röviden
    def ts():
        time.sleep(3)


    # Step0: Előfeltétel, belépés beépített tesztadattal
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

    # Step1: Popular tags kigyűjtése
    pop_tags = driver.find_elements_by_xpath('//div[@class="sidebar"]/div/a')
    with open('c:\\T360\\PycharmProjects\\selenium-py-peldatar\\selenium2-homework\\PopTagsExport.csv', "w",
              encoding='utf-8') as csvfile:
        # with open('./docs/testcases/PopTagsExport.csv', "w", encoding='utf-8') as csvfile:
        csvfile.write(f'Tag_name,Tag_href\n')
        for pt in pop_tags:
            csvfile.write(f'{pt.text},{pt.get_attribute("href")}\n')
            # print(f'{pt.text},{pt.get_attribute("href")}')

    driver.close()
    driver.quit()
