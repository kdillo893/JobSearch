from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sqlite3

company_prefix = "discover"
wd_ver = "wd5"
jobsTableExists = False

if (company_prefix is None or company_prefix == ""
        or wd_ver is None or wd_ver == ""):
    exit(-1)


def decodePwFile():
    return []


def initJobsTableDB():
    global jobsTableExists
    con = sqlite3.connect("jobs.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS
                jobapps(refid, company, title, status,
                        applydate, contactdate);
            ''')
    jobsTableExists = True
    pass


def writeToDB(obj):
    if isinstance(obj, dict):
        # check for db file, append
        con = sqlite3.connect("jobs.db")
        cur = con.cursor()

        # if the "jobs" table doesn't exist, create it
        if not jobsTableExists:
            initJobsTableDB()

        # table exists, insert a row
        cur.execute('''INSERT INTO jobapps
                    VALUES(12312, 'special company', 'Software Developer',
                           'APPLIED', now(), now());
                    ''')

    pass


def checkWorkdayApps(driver: webdriver.Chrome, company: str, wdver: str, creds):

    url = f'https://{company}.{wdver}.myworkdayjobs.com/en-US/Discover/userHome'
    driver.get(url)

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
        pwBox.send_keys("SECRET PASSWORD")
        submitButton.click()
        # todo
    else:
        print('bad thing')
        return

    # search by css button (does this scale from current or first instance?)
    # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    # text_box.send_keys("Selenium")

    # how to guarantee this is a button?
    # submit_button.click()

    # message = driver.find_element(by=By.ID, value="message")
    # text = message.text
    driver.implicitly_wait(10)

    # check the "candidate home" by navigating
    candidateHome = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "[data-automation-id='navigationItem-Candidate Home']"))
    )
    candidateHome.click()

    # read info on the row, send that to "write db" function
    jobsTable = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "[data-automation-id='applicationsSectionHeading']"))
    )

    # Grab each <tr> with attribute data-automation-id="taskListRow"
    # TODO

    writeToDB({"refid": 123123, "company": "Discover", "title": "SoftDev",
              "status": "", "applydate": 2024-11-22, "contactdate": 2024-11-22})

    pass


if __name__ == '__main__':
    # TODO: have parms with pw store...
    parms = decodePwFile()
    driver = webdriver.Chrome()

    checkWorkdayApps(driver, 'discover', 'wd5', None)

    driver.quit()
