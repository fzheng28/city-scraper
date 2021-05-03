#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
options = Options()
options.headless = True
b = webdriver.Chrome(options=options) 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select




###First page




b.get('https://wcca.wicourts.gov/advanced.html')




class_code = b.find_element_by_id("reactContent")




###start filing
b.execute_script("document.getElementsByName('filingDate.start')[0].value = '07-01-2020';")
start_filing=class_code.find_element_by_name('filingDate.start').get_attribute('value')




start_filing




###end filing
b.execute_script("document.getElementsByName('filingDate.end')[0].value = '07-08-2020';")
end_filing=class_code.find_element_by_name('filingDate.end').get_attribute('value')




end_filing




# Problem with class code: It has a dynamtic class which means when you click the box the class name and 
# attrbutes changes. When you put things in the box, for example, Small Claims - De Novo (31009), a new 
# name/section called classCode is created. 




# I tried to hard code the dynamtic page but it doesn't work. Some solutions online requres the usage of css/
#b.execute_script("document.getElementsByName('classCode')[0].value = '31004';")
# b.execute_script("document.getElementsByClassName('Select is-searchable Select--multi')[2].setAttribute('class','Select is-focused is-open is-searchable Select--multi')")
# b.execute_script("document.getElementsByClassName('Select-input')[3].setAttribute('aria-activedescendant', 'react-select-14--option-0')")
# b.execute_script("document.getElementsByClassName('Select-input')[3].setAttribute('aria-expanded', 'True')")
# b.execute_script("document.getElementsByClassName('Select-input')[3].setAttribute('aria-haspopup', 'True')")
# b.execute_script("document.getElementsByClassName('Select-input')[3].setAttribute('aria-owns', 'react-select-14--list react-select-14--backspace-remove-message')")
# b.execute_script("document.getElementsByClassName('Select-input')[3].value = 'Small Claims - De Novo (31009)';")




##click
# this is a sample code for the button, it only works if we have something selected in the classcode
#btn = b.find_elements_by_class_name("button button-spinner")
WebDriverWait(b,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".button.button-spinner"))).click()











################
# the next page

# from selenium.webdriver.support.select import Select




## show all the claims on one day 
# select_show = Select(driver.find_element_by_id("caseSearchResults_length"))
# select_show.select_by_index(-1)
#inside td there is tr that has a link to the last page use get_link 






###########################
### inside each claim





link='https://wcca.wicourts.gov/caseDetail.html?caseNo=2020SC017449&countyNo=40&index=0&isAdvanced=true'





b2 = webdriver.Chrome(options=options) 
b2.get(link)




## try to select filing date 
#ddIndl = b2.find_elements_by_css_selector('dl dd')
#b2.find_elements_by_xpath("//div[@class='cell-3 s-cell-12 field']//dd[0]")




### navigating the html to find defend (unsucessful attemps)
#home=b2.find_elements_by_id("home-container")
#home=b2.find_elements_by_css_selector("row main-content")
#b2.find_elements(By.cssSelector("dt.cell-3 s-cell-12 field"))
#main=b2.find_elements_by_css_selector('main')
#b2.find_elements_by_id("home-container")
#b2.find_elements_by_tag_name('td')





#main_div=main[0].find_elements_by_css_selector('div')
#main_div[0].find_elements_by_class_name('content-column')





#home[0].find_elements_by_id('summary')
#b2.find_elements_by_class_name("row main-content")
#b2.find_elements_by_xpath("//*[contains(text(), 'Defendant')]")




b.close()







