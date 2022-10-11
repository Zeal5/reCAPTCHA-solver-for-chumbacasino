import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from upload_images import upload_images
from selenium.common import exceptions
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
    opts.add_argument('--incognito')
else:
    opts.add_argument(fr"--user-data-dir={chrome_profile}")
driver = uc.Chrome(options=opts,use_subprocess=True)#
driver.maximize_window()



def sleep(waiting_time=5):
    driver.implicitly_wait(waiting_time)

def delete_sample_files():
        if os.path.exists("sample.mp3"):
            os.remove("sample.mp3")
        if os.path.exists("sample.wav"):
            os.remove("sample.wav")
        else:
            print("The file does not exist")
        time.sleep(5)

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
    open_page()
    delete_sample_files()
    time.sleep(5)

    if driver.current_url == "https://login.chumbacasino.com/":
        sleep()
        print("preparing to login...")
        log_in()
    
    sleep(15)
    print('Logged in successfully...')
    time.sleep(2)
    #daily reward pop-up 
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'daily-bonus__claim-btn'))).click()
        print("Claimed daily reward ")
    except exceptions.NoSuchElementException:
        print("daily reward already claimed")
    except exceptions.TimeoutException:
        print("daily reward already claimed")

    # start-up POPUP
    try:
        print("finding pop-ups...")
        hover = ActionChains(driver)
        hover_item = driver.find_element(By.ID,'offer__close')
        hover.move_to_element(hover_item).click().perform()
        print('closed the pop-up...')

    except exceptions.NoSuchElementException:
        print("No pop was detected ")
        sleep()

    #Click the postal code link from footer
    try:
        print('clicking Postal-Request-code Button from the page footer Section')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[3]/footer/div/ul[1]/li[5]/button'))).click()
    except exceptions.NoSuchElementException:
        print('Postal-Request-code Button was no on page reloading page and trying again...')
        return
    except exceptions.TimeoutException:
        print("coudln't find the Postal-Request-code Button on time reloading page...")
        return

    #click the get postal code button at 2nd last page
    time.sleep(3)
    try:
        print('Confiming to get the Postal-Request-code')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element(By.ID,'get-postal-request-code'))).click()
    except exceptions.NoSuchElementException:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(driver.find_element(By.ID,'get-postal-request-code'))).click()
        except exceptions.NoSuchElementException:
            print("coudn't find Postal-Request-code Button on 2nd last page reloading page...")
            return


    time.sleep(4)
    print('beginning to solvethe reCAPTCHA')
    #captcha solver here
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

    #switch to default iframe
        driver.switch_to.default_content()
    except exceptions.TimeoutException:
        print("Failed to locate reCAPTCHA reloading page...")
        return
    #switching to the select all images iframe
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div/div[4]/iframe")))

# a = driver.find_element(By.XPATH, '//*[@id="recaptcha-audio-button"]').click()
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-audio-button"]'))).click()
        print('Starting to Download the audio file...')
        ####here#####
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div/div[4]/iframe')))
        links = driver.find_element(By.XPATH, '/html/body/div/div/div[7]/a').get_attribute('href')

        captcha_solution = solve_captcha(links)
        if captcha_solution == None:
            print("reCaptcha unsolvable")
            return

        driver.find_element(By.XPATH,'/html/body/div/div/div[6]/input').send_keys(captcha_solution)
        sleep(5)
        driver.find_element(By.XPATH,'/html/body/div/div/div[8]/div[2]/div[1]/div[2]/button').click()
        time.sleep(3)
    except exceptions.StaleElementReferenceException:
        print('no captcha pop up was spoted')
    except exceptions.TimeoutException:
        print('no captcha pop up was spoted')

    #get postal code img
    generate_image_name = str(uuid.uuid4())
    print("saving screen Shot")
    driver.save_screenshot(f"screenshots\{generate_image_name}.png")
    print(f"imagae {generate_image_name} saved @ {time.strftime('%X')} sleeping for {delay} ")
    upload_images(str(generate_image_name))
    time.sleep(int(delay))



counter = 1
while True:
    try:
        request_postal_code()
        print("page out of sync Reloading...")
    except exceptions.WebDriverException:
        counter +=1
        print(f'{counter} something went wrong with WebDriver ???')
        continue
    except Exception:
        counter +=1
        print(f'{counter} some unknown Exception has occurd at {time.strftime("%X")} ???')
        continue




