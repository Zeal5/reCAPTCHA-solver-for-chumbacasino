import time
from selenium import common
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium import common
from selenium.webdriver.common.keys import Keys
from Convert_to_text import solve_captcha
from dotenv import load_dotenv
import os
import uuid
#load variables
load_dotenv()
email = os.getenv('email')
paswd = os.getenv('paswd')
chrome_profile = os.getenv('Chrome_profile')
delay = os.getenv('Delay')

#start browser
opts = uc.ChromeOptions()
if chrome_profile == 'None':
    opts.add_argument('incognito')
else:
    opts.add_argument(fr"--user-data-dir={chrome_profile}")
driver = uc.Chrome(options=opts,use_subprocess=True)#
driver.maximize_window()



def sleep(waiting_time=5):
    driver.implicitly_wait(waiting_time)

def delete_sample_files():
        if os.path.exists("sample.mp3"):
            os.remove("sample.mp3")
            os.remove("sample.wav")
        else:
            print("The file does not exist")

#goto page
def open_page():
    driver.get('https://lobby.chumbacasino.com/')
    
#log into website
def log_in():
    print('entring email')
    driver.find_element(By.ID,'login_email-input').send_keys(email)
    print('entring paswd')
    driver.find_element(By.ID,'login_password-input').send_keys(paswd)
    driver.find_element(By.ID,'login_submit-button').click()
    time.sleep(5)

#goto Postal request code

def request_postal_code():
    time.sleep(int(delay))
    open_page()
    delete_sample_files()
    if driver.current_url == "https://login.chumbacasino.com/":
        log_in()
    print('was logged in')
    time.sleep(15)

    # start-up POPUP
    try:
        print('trying to close pop up')
        hover = ActionChains(driver)
        hover_item = driver.find_element(By.ID,'offer__close')
        print('hovering over item')
        
        hover.move_to_element(hover_item).click().perform()
    except common.exceptions.NoSuchElementException:
        print("sleeping instead of closning the pop up")
        sleep()

    #Click the postal code link from footer
    try:
        print('trying Try block')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[3]/footer/div/ul[1]/li[5]/button'))).click()
        sleep(20)
    except common.exceptions.NoSuchElementException:
        print('trying except block')
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/footer/div/ul[1]/li[5]/button').click()
    #click the get postal code button at 2nd last page
    print('entering 2nd last page')
    
    driver.find_element(By.ID,'get-postal-request-code').click()

    time.sleep(8)
    print('clicking the check-box')
    #captcha solver here
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

    #switch to default iframe
    driver.switch_to.default_content()

    #switching to the select all images iframe
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div/div[4]/iframe")))
    print('fetching the url')
    a = driver.find_element(By.XPATH, '//*[@id="recaptcha-audio-button"]').click()
    print('got element')
    ####here#####
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div/div[4]/iframe')))
    links = driver.find_element(By.XPATH, '/html/body/div/div/div[7]/a').get_attribute('href')

    captcha_solution = solve_captcha(links)
    if captcha_solution == None:
        return

    driver.find_element(By.XPATH,'/html/body/div/div/div[6]/input').send_keys(captcha_solution)
    sleep(5)
    driver.find_element(By.XPATH,'/html/body/div/div/div[8]/div[2]/div[1]/div[2]/button').click()
    time.sleep(3)

    #get postal code img

    driver.save_screenshot(f"screenshots\{str(uuid.uuid4())}.png")


    #get the postal code
# try:
#     code = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/p[2]').text
#     print(code)
# except common.exceptions.NoSuchElementException:
#     print('restarting')
#     return

# if code is not None:
#     with open('postal_codes.txt','a+') as file:
#         file.write(f"{code}\n")
    
while True:
    request_postal_code()


