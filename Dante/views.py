from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from gensim.summarization import  summarize


def home(request):
    return render(request, 'Dante/home.html')


def results(request):
    context = request.POST
    title = {"title": openChromeAndVisitBing(context['sq'])}
    return render(request, 'Dante/results.html', title)




def openChromeAndVisitBing(query):
    options = ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    # options.headless = True
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.bing.com')
    wait = WebDriverWait(driver, 5)
    wait2 = WebDriverWait(driver, 10)
    # wait for pop up to appear then click on it
    men_menu = wait.until(ec.visibility_of_element_located((By.ID, 'bnp_btn_accept')))
    men_menu.click()
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys(query)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    boDy = driver.find_element_by_id('b_results')
    lis = boDy.find_elements_by_css_selector('li')
    hrefs = []
    for li in lis:
        aLink = li.find_element_by_css_selector('a')
        href = aLink.get_attribute('href')
        if href is not None and href.startswith('ht'):
            hrefs.append(href)
    finalText = openLinks(hrefs, query)
    return finalText

def openLinks(links, query):
    print(len(links))
    pageText = ''
    for i in range(0, 1):
        options = ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        # options.headless = True
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(links[i])
        elements = driver.find_elements_by_css_selector('*')
        for element in elements:
            if not element.text:
                pageText += ''
            else:
                pageText += element.text
        driver.quit()
    summarized_text = summarize(pageText, ratio=0.3)
    final_summarized_text = summarize(summarized_text, ratio=0.1)
    return final_summarized_text
