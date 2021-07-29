# CON_TC23_Pages: Több oldalas lista bejárása

# a szükséges csomagok, modulok betöltése
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_CON_TC23_Pages():
    # webdriver konfiguráció, tesztelt oldal megnyitása
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("http://localhost:1667")

    # tesztre vonatkozó egységes, központi időzítés
    def ts():
        time.sleep(3)

    # Step0: Előfeltétel, tesztadatok, belépés létező felhasználóval
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
    art_per_pages = []

    # Step2: Oldalon belüli bejegyzések ellenőrzése
    #       (az utolsó oldal utolsó eleme egyezik-e az első oldal utolsó elemével,
    #       több oldalnál az oldalak elemszámai egyeznek-e az utolsó kivételével)

    for i in range(len(pages)):
        pages[i].click()
        ts()
        articles = driver.find_elements_by_xpath('//div[@class="article-preview"]')
        # az első oldal utolsó elemének meghatározása
        if i == 0:
            ts()
            last_art_first_page = articles[-1]
            text1 = last_art_first_page.find_element_by_xpath('a/h1').text
            href1 = last_art_first_page.find_element_by_xpath('a').get_attribute('href')
        # az utolsó oldal utolsó elemének meghatározása
        if i == len(pages) - 1:
            last_art_last_page = articles[-1]
            text2 = last_art_last_page.find_element_by_xpath('a/h1').text
            href2 = last_art_last_page.find_element_by_xpath('a').get_attribute('href')
        print(f"{i + 1}.oldal bejegyzéseinek száma {len(articles)}")
        art_per_pages.append(len(articles))

    # ugyanannak a tételnek az első és utolsó oldalon való vzsgálata
    try:
        print(text1, ' ', text2)
        print(href1, '  ', href2)
        assert text1 == text2
        assert href1 == href2
        print('Azonos tétel több oldalon!')
    except:
        pass

    # több oldalnál a kilistázott mennyiségek vizsgálata
    try:
        if len(pages) > 2:
            assert art_per_pages[0] != art_per_pages[1]
        print('Eltérő tételmennyiség az oldalakon!')
    except:
        pass

    # ablak lezárása, memória felszabadítása
    driver.close()
    driver.quit()
