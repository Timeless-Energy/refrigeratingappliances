'''
python python-3.11.6-amd64
pip freeze > requirements.txt
pip install -r requirements.txt
'''

import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from collections import ChainMap
import browser_chrome
import data_classification
import json


with open('config.json') as json_file:
    config_efficiency_class = ChainMap(json.load(json_file))
    # print(config_efficiency_class)

a = config_efficiency_class['A']
b = config_efficiency_class['B']
c = config_efficiency_class['C']
d = config_efficiency_class['D']
e = config_efficiency_class['E']
f = config_efficiency_class['F']
g = config_efficiency_class['G']

path_database = None
if a and b and c and d:
    path_database = 'Archiv\\A_B_C_D'
if e:
    path_database = 'Archiv\\E'
if f:
    path_database = 'Archiv\\F'
if g:
    path_database = 'Archiv\\G'
print(path_database)

''' Energy Efficiency Class '''
def energy_efficiency_class(a, b, c, d, e, f, g):
    ''' dropdown open '''
    dropdown_energy_efficiency_open = WebDriverWait(driver, 5).until(
        EC.visibility_of_any_elements_located((
            By.CSS_SELECTOR,
            "button.eui-u-text-center"
        )))
    dropdown_energy_efficiency_open[0].click()

    ''' select A-D '''
    efficiency_class = WebDriverWait(driver, 6).until(
        EC.visibility_of_all_elements_located((
            By.CSS_SELECTOR,
            "span.ux-tree__leaf.ng-star-inserted"
        )))
    if a:
        efficiency_class[0].click()
    if b:
        efficiency_class[1].click()
    if c:
        efficiency_class[2].click()
    if d:
        efficiency_class[3].click()
    if e:
        efficiency_class[4].click()
    if f:
        efficiency_class[5].click()
    if g:
        efficiency_class[6].click()
    time.sleep(1)

    ''' dropdown close '''
    button = driver.find_element(By.CSS_SELECTOR, 'div.cdk-overlay-backdrop')
    button.click()

    ''' button search '''
    button = driver.find_element(By.CSS_SELECTOR, 'button.pull-right.ecl-button--primary.ecl-button')
    button.send_keys(Keys.ENTER)
    return

def number_page():
    dropdown_energy_efficiency_open = WebDriverWait(driver, 1).until(
        EC.visibility_of_any_elements_located((
            By.CSS_SELECTOR,
            "select.ecl-select.ng-valid"
        )))
    dropdown_energy_efficiency_open[0].send_keys(Keys.ARROW_DOWN, Keys.DOWN, Keys.DOWN)
    return

''' Fridges, freezers and wine storage (29 131)  '''
def number_of_appliances_check():
    number_of_appliances_check = driver.find_element(By.CSS_SELECTOR, "h2.ecl-u-type-heading-2").text
    appliances_total = int(''.join(filter(str.isdigit, number_of_appliances_check)))
    return appliances_total


APPLIANCES_PER_PAGE = '100'
def number_of_appliances_per_page():
    page_number_of_next = int(
        (int(appliances_total) / int(APPLIANCES_PER_PAGE)) + (int(appliances_total) % int(APPLIANCES_PER_PAGE) > 0))
    print("Appliances total: " + str(appliances_total))
    print("Appliance per Site: " + str(APPLIANCES_PER_PAGE))
    print("Site total: " + str(page_number_of_next) + '\n')
    return page_number_of_next


''' start chrome'''
driver = browser_chrome.start_chrome()
energy_efficiency_class(a, b, c, d, e, f, g)
time.sleep(3)
number_page()
time.sleep(1)
appliances_total = number_of_appliances_check()
page_number_of_next = number_of_appliances_per_page()
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


''' Read Excel File all appliances '''
def read_excel_data_base_all_appliances(a, b, c, d, e, f, g):
    df2 = None
    if a and b and c and d:
        df2 = pd.read_excel(path_database + '\data_base_all_appliances_A_B_C_D_.xlsx')
    if e:
        df2 = pd.read_excel(path_database + '\data_base_all_appliances_E_.xlsx')
    if f:
        df2 = pd.read_excel(path_database + '\data_base_all_appliances_F_.xlsx')
    if g:
        df2 = pd.read_excel(path_database + '\data_base_all_appliances_G_.xlsx')

    excel_total = [list(row) for row in df2.values]
    excel_total.insert(0, df2.columns.to_list())
    return excel_total


''' Read Excel File all name type '''
def read_excel_data_base_all_name_type(a, b, c, d, e, f, g):
    df1 = None
    if a and b and c and d:
        df1 = pd.read_excel(path_database + '\data_base_all_name_type_A_B_C_D_.xlsx')
    if e:
        df1 = pd.read_excel(path_database + '\data_base_all_name_type_E_.xlsx')
    if f:
        df1 = pd.read_excel(path_database + '\data_base_all_name_type_F_.xlsx')
    if g:
        df1 = pd.read_excel(path_database + '\data_base_all_name_type_G_.xlsx')

    supplier_type_excel = [list(row) for row in df1.values]
    supplier_type_excel.insert(0, df1.columns.to_list())
    # print("supplier_type_excel: " + str(supplier_type_excel))
    return supplier_type_excel


appliance_name_total = read_excel_data_base_all_appliances(a, b, c, d, e, f, g)
supplier_type_excel = read_excel_data_base_all_name_type(a, b, c, d, e, f, g)

list_of_appliances = []
list_of_name_type = []
data_base_ref_appliances = None
data_base_excel = None

''' ----------------- If it was error, you can start page an the last count --------------------------- '''
count = 0  # z.B. 14
if count > 0:
    start_page = 1
    while start_page < count:
        ''' scroll down '''
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        ''' read button Next> '''
        links_next_all = WebDriverWait(driver, 2).until(
            EC.visibility_of_all_elements_located((
                By.CSS_SELECTOR,
                "a.ecl-pagination__link.ecl-link.ecl-link--standalone.ecl-link--icon.ecl-link--icon-after.ng-star-inserted"
            )))
        print("links_next_all: " + str(len(links_next_all)))
        ''' click Next> '''
        if len(links_next_all) == 1:
            links_next_all[0].click()
        if len(links_next_all) == 2:
            links_next_all[1].click()
        time.sleep(2)

        start_page = start_page + 1
        print("start_page: " + str(start_page))
        print("count1: " + str(count))

''' -------------------- Data Base ------------------------------ '''
page_number_of_next_step = page_number_of_next
count_type = 0
while count <= page_number_of_next_step:
    ''' -------------------- local time --------------------------- '''
    t = time.localtime()
    date_now = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday) + str(t.tm_hour)
    date_now2 = str(t.tm_year) + str(".") + str(t.tm_mon) + str(".") + str(t.tm_mday)
    print("date_now: " + str(date_now2))
    time_start_data_now = time.time()
    ''' scroll down '''
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    ''' --------------- check type with database -----------------------'''
    ''' read all elements type on this page as number '''
    # number_all_type_of_this_page = driver.find_elements(By.CSS_SELECTOR, 'span.ecl-u-type-l')
    number_all_type_of_this_page = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((
            By.CSS_SELECTOR,
            "span.ecl-u-type-l"
        )))
    number_of_elements_type = len(number_all_type_of_this_page)    
    print("number_of_elements_type:" + str(number_of_elements_type))
    ''' read each element type '''
    # print("len(number_all_type_of_this_page): " + str(number_of_elements_type))
    for index_type in range(number_of_elements_type):
        # read_elements_type = driver.find_elements(By.CSS_SELECTOR, 'span.ecl-u-type-l')
        read_elements_type = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((
                By.CSS_SELECTOR,
                "span.ecl-u-type-l"
            )))
        # print("index_type: " + str(index_type))
        name_type = read_elements_type[index_type].text
        # print("name_type: " + str(name_type))
        name_type_string = ("".join(map(str, name_type)))

        ''' --------- index_check_of_exist in supplier_type_excel -------------- '''
        result_name_type = False
        for index_check_of_exist in supplier_type_excel:
            index_check_of_exist_string = (" ".join(map(str, index_check_of_exist)))

            if name_type_string == index_check_of_exist_string:
                # print("name_type_string == index_check_of_exist_string: " + str(name_type_string) + " == " + str(index_check_of_exist_string))
                result_name_type = True
                break

        if not result_name_type:
            time_start = time.time()
            ''' scroll down '''
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            ''' ---------------------- Click button: "Details>" -------------------------------- '''
            # elements_from_main_site = driver.find_elements(By.CLASS_NAME, "ecl-button.ecl-button--primary")
            elements_from_main_site = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "button.ecl-button.ecl-button--primary"
                )))
            # print("elements_from_main_site: " + str(len(elements_from_main_site)))
            ''' click Details> '''
            # print("index_type click: " + str(index_type))
            ''' index_type = 0, Button Details = 2
                index_type = 1, Button Details = 4
                index_type = 2, Button Details = 6
                index_type = 3, Button Details = 8
                index_type = 4, Button Details = 10
                index_type = 5, Button Details = 12
            '''
            button_Details = (index_type + 2)
            # print("index_type: " + str(index_type))
            # print("button_Details: " + str(button_Details))
            button_Details = (button_Details + index_type)
            # print("button_Details = button_Details + index_type: " + str(button_Details))
            elements_from_main_site[button_Details].click()

            ''' ---------------------- Page name of appliance" ---------------------------------- '''
            ''' scroll down '''
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            ''' supplier name: z.B. CORBERO '''
            # name_supplier = driver.find_elements(By.CLASS_NAME, "ecl-u-type-l").text
            name_supplier = WebDriverWait(driver, 7).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "div.ecl-u-type-l"
                ))).text
            print("name_supplier: " + str(name_supplier))
            ''' Date '''
            list_of_appliances.append(date_now2)
            ''' supplier '''
            list_of_appliances.append(name_supplier)

            ''' supplier type: z.B. CCM200834NFW'''
            # appliance_type = driver.find_elements(By.CLASS_NAME, "ecl-u-d-inline-block").text
            appliance_type = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    "div.ecl-u-d-inline-block"
                ))).text
            print("appliance_type: " + str(appliance_type))
            ''' type '''
            list_of_appliances.append(appliance_type)
            # print("list_of_appliances: " + str(list_of_appliances))
            list_of_name_type.append(appliance_type)

            ''' scroll down '''
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            ''' ----------------------------------- append to database --------------------------------------------'''
            ''' ---- all elements: Low-noise appliance, Wine storage appliance ... ---- '''
            List_Low_noise_appliance = []
            items_list = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "div.ecl-row.ecl-u-flex-grow-1"
                )))
            number_items_list = (len(items_list))
            for index_intems_list in range(number_items_list):
                List_Low_noise_appliance.append(items_list[index_intems_list].text)
            # print("List_Low_noise_appliance: " + str(List_Low_noise_appliance))

            ''' ---- all values for elements: Low-noise appliance, Wine storage appliance ... ---- '''
            Value_Low_noise_appliance = []
            elements_from_supplier_site = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "span.ecl-u-type-bold.ecl-u-pl-l-xl.ecl-u-pr-2xs.ecl-u-type-align-right"
                )))
            number_elements_from_supplier_site = len(elements_from_supplier_site)
            for index_elements_from_supplier_site in range(number_elements_from_supplier_site):
                Value_Low_noise_appliance.append(elements_from_supplier_site[index_elements_from_supplier_site].text)
            # print("Value_Low_noise_appliance: " + str(Value_Low_noise_appliance))

            ''' ---- all COMPARTMENT 1, 2, 3 ---- '''
            headline_array = []
            all_headline = WebDriverWait(driver, 2).until(
                EC.visibility_of_all_elements_located((
                    By.CSS_SELECTOR,
                    "span.ux_header_dashed_line"
                )))
            number_all_headline = (len(all_headline))
            for index_all_headline in range(number_all_headline):
                if all_headline[index_all_headline].text != "LIGHT SOURCE PARAMETERS":
                    headline_array.append(all_headline[index_all_headline].text)
            # print("headline_array: " + str(headline_array))

            for index in range(len(List_Low_noise_appliance)):
                ''' ---------------- TYPE OF REFRIGERATING APPLIANCE --------------  '''
                if "Low-noise" in List_Low_noise_appliance[index] :
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if "Wine storage" in List_Low_noise_appliance[index]:
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if "Other refrigerating" in List_Low_noise_appliance[index]:
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if "Design" in List_Low_noise_appliance[index] :
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                ''' ---------------- GENERAL PRODUCT PARAMETERS -------------------- '''
                if List_Low_noise_appliance[index] == "Overall dimensions":
                    overall_dimensions = Value_Low_noise_appliance[index]
                    # print("elements_from_supplier_site[index2]:" + str(elements_from_supplier_site[index2].text))
                    overall_dimensions = (''.join(filter(str.isalnum, overall_dimensions)))
                    # print("overall_dimensions:" + str(overall_dimensions))
                    overall_dimensions = overall_dimensions.replace('Heightx', ' ')
                    overall_dimensions = overall_dimensions.replace('Widthx', ' ')
                    overall_dimensions = overall_dimensions.replace('Depth', ' ')
                    overall_dimensions = overall_dimensions.split()
                    list_of_appliances.append(int(overall_dimensions[0]))
                    list_of_appliances.append(int(overall_dimensions[1]))
                    list_of_appliances.append(int(overall_dimensions[2]))
                if List_Low_noise_appliance[index] == "Total volume":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Energy efficiency Index (EEI)":
                    # energy_efficiency_index = (''.join(filter(str.isalnum, Value_Low_noise_appliance[index].text)))
                    # list_of_appliances.append(int(energy_efficiency_index))
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Airborne acoustical noise emissions":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Airborne acoustical noise emission class":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Annual energy consumption":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Climate class":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Minimum ambient temperature for which the refrigerating appliance is suitable":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Maximum ambient temperature for which the refrigerating appliance is suitable":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                if List_Low_noise_appliance[index] == "Winter setting":
                    list_of_appliances.append(Value_Low_noise_appliance[index])
                ''' ---------------- FOR 4-STAR COMPARTMENTS ------------------------'''
                if List_Low_noise_appliance[index] == "Fast freeze facility":
                    list_of_appliances.append(Value_Low_noise_appliance[index])

            ''' ------------- COMPARTMENT #1, #2, etc.  --------------- '''
            for index2 in range(len(List_Low_noise_appliance)):
                if List_Low_noise_appliance[index2] == "Compartment Volume":
                    # print("------------- COMPARTMENT #1, #2, etc.  ---------------")
                    if len(headline_array) >= 1:
                        ''' 0,1,2,3 '''
                        list_of_appliances.append(headline_array[0])
                    items_list_end = len(List_Low_noise_appliance) - index2
                    for index3 in range(items_list_end):
                        if index3 == 4 and len(headline_array) >= 2:
                            ''' 4,5,6,7 '''
                            list_of_appliances.append(headline_array[1])
                        if index3 == 8 and len(headline_array) >= 3:
                            ''' 8,9,10,11 '''
                            list_of_appliances.append(headline_array[2])
                        if index3 == 12 and len(headline_array) >= 4:
                            ''' 12,13,14,15 '''
                            list_of_appliances.append(headline_array[3])
                        if index3 == 16 and len(headline_array) >= 5:
                            ''' 16,17,18,19 '''
                            list_of_appliances.append(headline_array[4])
                        list_of_appliances.append(List_Low_noise_appliance[index2 + index3])
                        list_of_appliances.append(Value_Low_noise_appliance[index2 + index3])
                    break

            appliance_name_total.append(list_of_appliances)
            list_of_appliances = []

            supplier_type_excel.append(list_of_name_type)
            list_of_name_type = []

            ''' ------------------------------------ Save Excel File --------------------------------------------'''
            energy_class_output = '_'
            for efficiency_class, value in config_efficiency_class.items():
                # print(efficiency_class, value)
                if value:
                    energy_class_output = energy_class_output + efficiency_class
                    energy_class_output = energy_class_output + '_'

            ''' Save Excel File '''
            data_base_ref_appliances = pd.DataFrame(appliance_name_total)
            file_name_excel = (path_database + '\data_base_all_appliances' + energy_class_output + date_now + '.xlsx')
            print("Excel File 'data_base_all_appliances + date_now' is saving ... , don't interrupt!")
            data_base_ref_appliances.to_excel(file_name_excel, index=False, header=False)
            print("successfully saved!")

            print("Excel File 'data_base_all_appliances' is saving ... , don't interrupt!")
            data_base_ref_appliances.to_excel(path_database + '\data_base_all_appliances' + energy_class_output + '.xlsx', index=False, header=False)
            print("successfully saved!")

            data_base_excel = pd.DataFrame(supplier_type_excel)
            print("Excel File 'data_base_all_name_type' is saving ... , don't interrupt!")
            data_base_excel.to_excel(path_database + '\data_base_all_name_type' + energy_class_output + '.xlsx', index=False, header=False)
            print("successfully saved!")

            ''' time per count'''
            time_stop = time.time()
            time_total = time_stop - time_start
            print("time_total: " + str(time_total))

            ''' ------------------------- restart browser --------------------------------'''
            if count_type >= 60:
                count_type = 0
                print("read_page_number: " + str(count_type))
                driver.close()
                time.sleep(2)
                driver.quit()
                time.sleep(5)
                print("restart")

                ''' start_chrome '''
                driver = browser_chrome.start_chrome()
                time.sleep(3)
                energy_efficiency_class(a, b, c, d, e, f, g)
                time.sleep(3)
                number_page()
                time.sleep(1)
                appliances_total = number_of_appliances_check()
                time.sleep(3)
                page_number_of_next = number_of_appliances_per_page()
                ''' data_base_all_appliances.xlsx '''
                appliance_name_total = read_excel_data_base_all_appliances(a, b, c, d, e, f, g)
                ''' data_base_all_name_type.xlsx '''
                supplier_type_excel = read_excel_data_base_all_name_type(a, b, c, d, e, f, g)

                current_page = 1
                while current_page < count:
                    ''' scroll down '''
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    ''' read button Next> '''
                    links_next_all = WebDriverWait(driver, 2).until(
                        EC.visibility_of_all_elements_located((
                            By.CSS_SELECTOR,
                            "a.ecl-pagination__link.ecl-link.ecl-link--standalone.ecl-link--icon.ecl-link--icon-after.ng-star-inserted"
                        )))
                    # print("links_next_all: " + str(len(links_next_all)))
                    ''' click Next> '''
                    if len(links_next_all) == 1:
                        links_next_all[0].click()
                    if len(links_next_all) == 2:
                        links_next_all[1].click()

                    time.sleep(2)

                    current_page = current_page + 1
                    print("current_page : " + str(current_page))
                    print("count2: " + str(count))

            else:
                ''' return to the next page '''
                count_type = count_type + 1
                print("count_type --> : " + str(count_type))
                driver.back()
                print("driver.back")

    ''' scroll down '''
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

    ''' scroll down '''
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    ''' read button Next> '''
    print("read button: Next>")

    if count < page_number_of_next:
        links_next_all = WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((
                By.CSS_SELECTOR,
                "a.ecl-pagination__link.ecl-link.ecl-link--standalone.ecl-link--icon.ecl-link--icon-after.ng-star-inserted"
            )))
        ''' click Next> '''
        if len(links_next_all) == 1:
            links_next_all[0].click()
        if len(links_next_all) == 2:
            links_next_all[1].click()

    count = count + 1
    print("count3: " + str(count))
    print("page_number_of_next:" + str(page_number_of_next))

    print(list_of_appliances)
    time_stop2 = time.time()
    time_total2 = time_stop2 - time_start_data_now
    print("time_total2: " + str(time_total2))

driver.close()
driver.quit()

''' ----------------------------- classify data base -------------------------- '''
data_classification.start_classify(a, b, c, d, e, f, g)
print("classify completed")

# https://bot.sannysoft.com/


