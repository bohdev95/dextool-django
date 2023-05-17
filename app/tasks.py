from huey import crontab
from huey.contrib.djhuey import periodic_task, task
import csv
import requests
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium_recaptcha_solver import RecaptchaSolver, StandardDelayConfig
import time
import pytest
import os
from .utils import *
from .models import *
from django.utils.timezone import make_aware

CSV_URL = 'https://etherscan.io/exportData?type=tokenholders&contract=0xfb7b4564402e5500db5bb6d63ae671302777c75a&decimal=0'

CAPTCHA_KEY = "92a71bdc5752c5abc369a6389cdf77d8"

DOWNLOAD_PATH = "C:\\Users\Admin\Downloads"

CSV_FILENAME = 'export-tokenholders-for-contract-0xfb7b4564402e5500db5bb6d63ae671302777c75a'

@task()
def hello_task():
    print("hello wold")

@periodic_task(crontab(minute='*/10'))
def every_one_mins():
    print('every_one_mins')
    project_list = Projects.objects.filter(status=1).values()

    for project in project_list:
        CSV_FILENAME = project['file_name']
        CSV_URL = project['download_url']
       
        summary_bins = project['summary_bins']

        for root, dirs, files in os.walk(DOWNLOAD_PATH):
            for file in files:
                if CSV_FILENAME in file:
                    os.remove(os.path.join(root, file))
    
        options = webdriver.ChromeOptions()

        options.add_argument("--headless")
        options.add_argument('--incognito')

        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")


        driver = webdriver.Chrome()
        driver.maximize_window()
        
        solver = RecaptchaSolver(driver=driver)

        driver.get(CSV_URL)

        
        btnCookie =driver.find_element(By.ID, "btnCookie")
        btnCookie.click()

        VIEWSTATE = ""
        VIEWSTATE = driver.find_element(By.XPATH, '//input[@id="__VIEWSTATE"]').get_attribute('value')
        
        VIEWSTATEGENERATOR = ""
        VIEWSTATEGENERATOR = driver.find_element(By.XPATH, '//input[@id="__VIEWSTATEGENERATOR"]').get_attribute('value')
        
        EVENTVALIDATION = ""
        EVENTVALIDATION = driver.find_element(By.XPATH, '//input[@id="__EVENTVALIDATION"]').get_attribute('value')
        

        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

        iframe_src = recaptcha_iframe.get_attribute("src")

        temp =  iframe_src.split("&k=")[1]
        googlekey = temp.split("&co=")[0]
        
        url = "http://2captcha.com/in.php?key="+CAPTCHA_KEY+"&method=userrecaptcha&googlekey="+googlekey+"&pageurl="+CSV_URL
        response = requests.get(url)
        Captcha_ID = response.content.decode('utf-8').split("OK|")[1]

        response = "CAPCHA_NOT_READY"
        while(response == "CAPCHA_NOT_READY"):
            time.sleep(5)
            response = get_recapture_response(Captcha_ID)
            print(response)
        
        recapture_response = response.split("OK|")[1]


        driver.execute_script("var new_form = document.body.appendChild(document.createElement('form')); new_form.action = './exportData?type=tokenholders&contract=0xfb7b4564402e5500db5bb6d63ae671302777c75a&decimal=0'; new_form.method='post'; var new_VIEWSTATE = document.createElement('input'); new_VIEWSTATE.type = 'text'; new_VIEWSTATE.name = '__VIEWSTATE'; new_VIEWSTATE.value = '"+VIEWSTATE+"'; new_form.appendChild(new_VIEWSTATE); var new_VIEWSTATEGENERATOR = document.createElement('input'); new_VIEWSTATEGENERATOR.type = 'text'; new_VIEWSTATEGENERATOR.name = '__VIEWSTATEGENERATOR'; new_VIEWSTATEGENERATOR.value = '"+VIEWSTATEGENERATOR+"'; new_form.appendChild(new_VIEWSTATEGENERATOR); var new_EVENTVALIDATION = document.createElement('input'); new_EVENTVALIDATION.type = 'text'; new_EVENTVALIDATION.name = '__EVENTVALIDATION'; new_EVENTVALIDATION.value = '"+EVENTVALIDATION+"'; new_form.appendChild(new_EVENTVALIDATION); var new_g_recaptcha_response = document.createElement('input'); new_g_recaptcha_response.type = 'text'; new_g_recaptcha_response.name = 'g-recaptcha-response'; new_g_recaptcha_response.value = '"+recapture_response+"'; new_form.appendChild(new_g_recaptcha_response); var new_ContentPlaceHolder1_btnSubmit = document.createElement('input'); new_ContentPlaceHolder1_btnSubmit.type = 'submit'; new_ContentPlaceHolder1_btnSubmit.name = 'ctl00$ContentPlaceHolder1$btnSubmit'; new_ContentPlaceHolder1_btnSubmit.id = 'new_ContentPlaceHolder1_btnSubmit'; new_ContentPlaceHolder1_btnSubmit.value = 'Download'; new_form.appendChild(new_ContentPlaceHolder1_btnSubmit);")
        # post_data = {
        #     "__VIEWSTATE": VIEWSTATE,
        #     "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
        #     "__EVENTVALIDATION": EVENTVALIDATION,
        #     "g-recaptcha-response": recapture_response,
        #     "tl00$ContentPlaceHolder1$btnSubmit": "Download"
        # }

        # solver.click_recaptcha_v2(iframe=recaptcha_iframe)

        while (True):
            time.sleep(5)
            Download_btn = driver.find_element(By.ID, "new_ContentPlaceHolder1_btnSubmit")
            try:
                Download_btn.click()
                print("available")
                break
            except:
                print("not available")

        time.sleep(180)
        
        driver.quit()

        total_supply = 100000000
        now = make_aware(datetime.datetime.today())

        print(summary_bins.split(','))
        bins_array = summary_bins.split(',')
        for i in range(len(bins_array)):
            bins_array[i] = int(bins_array[i])


        summary_table = Summary_table(file = DOWNLOAD_PATH + '\\' + CSV_FILENAME + ".csv", total_supply=total_supply, bins=bins_array)

        for i in range(len(summary_table)):
                row = summary_table.iloc[i]
                ttt = now.strftime("%Y-%m-%d")
                data = Data.objects.filter(timestamp=ttt).values()
                if(data.count() > 0):
                    Data.objects.filter(timestamp=ttt).delete()

                for i in range(len(summary_table)):
                    row = summary_table.iloc[i]
                    processed_data = Data.objects.create(
                        timestamp=ttt,
                        supply=total_supply,
                        category=row["category"],
                        number_of_addresses=row["number_of_addresses"],
                        sum_of_balances=row["sum_of_balances"],
                        average_balance=row["average_balance"],
                        percent_of_supply=row["percent_of_supply"],
                        project_id=project['id']
                    )
                    processed_data.save()
            
            # save the processed row to the database
            

    # response = scraper.post(CSV_URL, data=post_data, stream=True, timeout=600)
    
    # print(response.content.decode('utf-8'))


    # time.sleep(60)

def get_recapture_response(Captcha_ID):
    url = "http://2captcha.com/res.php?key="+CAPTCHA_KEY+"&action=get&id="+Captcha_ID
    response = requests.get(url)
    return response.content.decode('utf-8')