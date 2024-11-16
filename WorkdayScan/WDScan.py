from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

company_prefix = "discover"
wd_ver = "wd5"

if (company_prefix is None or company_prefix == ""
        or wd_ver is None or wd_ver == ""):
    exit(-1)

driver = webdriver.Chrome()

driver.get("https://discover.wd5.myworkdayjobs.com/en-US/Discover/userHome")

# wait time for load?
title = driver.title
print(title)

# get element by name attribute (form related searching)
# text_box = driver.find_element(by=By.NAME, value="my-text")
# custom finder for workday
emailBox = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id='email']"))
)

if emailBox is not None:
    pwBox = driver.find_element(By.CSS_SELECTOR,
                                "[data-automation-id='password']")
    submitButton = driver.find_element(By.CSS_SELECTOR,
                                       "[data-automation-id='click_filter']")

    print(emailBox)
    print(pwBox)
    print(submitButton)

    emailBox.send_keys("kdillo893@gmail.com")
    pwBox.send_keys("dildo")
    submitButton.click()
    # todo

# search by css button (does this scale from current or first instance?)
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
# text_box.send_keys("Selenium")

# how to guarantee this is a button?
# submit_button.click()

# message = driver.find_element(by=By.ID, value="message")
# text = message.text
driver.implicitly_wait(10)

driver.quit()
