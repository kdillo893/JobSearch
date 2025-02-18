from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sqlite3

company_prefix = "discover"
wd_ver = "wd5"
APPS_DB = "applications.db"

if (company_prefix is None or company_prefix == ""
        or wd_ver is None or wd_ver == ""):
    exit(-1)


def getAppDbConnection():
    return sqlite3.connect(APPS_DB)


def tableExists(tableName):
    con = getAppDbConnection()
    cur = con.cursor()

    res = cur.execute(
        "SELECT name FROM sqlite_schema WHERE tbl_name = ?", tableName)
    name = res.fetchone()
    con.close()

    if (name == tableName):
        return True

    return False


def initJobsTableDB():
    con = getAppDbConnection()
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS
                companies(company_id NOT NULL, company_name, workday_prefix,
                        careers_url);
            ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS
                applications(job_reqid, company_id, title, status,
                        applied, updated, unique(job_reqid, company_id));
            ''')
    con.close()
    pass


def appStatusToInt(appStatus):
    if appStatus in ["No Longer Under Consideration", "Not Selected"]:
        return 1
    elif appStatus == "Pending":
        return 0
    elif appStatus == "Not Submitted":
        return 2
    else:
        return 3
    pass


def appStatusFromInt(appStatusInt):
    if appStatusInt == 1:
        return "Rejected"
    elif appStatusInt == 0:
        return "Applied"
    elif appStatusInt == 2:
        return "Bad Status"
    else:
        return "Uh oh"


def writeApplicationsToDb(apps):

    # with the array "apps", construct the sql statement for adding
    # 1. get db entries that match job_reqid and company_id of "apps" elements

    query = "SELECT job_reqid, company_id FROM applications WHERE "
    query += " OR ".join([f"job_reqid = {a["job_repid"]} AND company = {a["company"]}" for a in apps])
    query += ";"
    print(query)

    con = getAppDbConnection()
    print(sqlite3.complete_statement(query))

    # 2. filter out the from the apps list anything in the matched query
    cur = con.cursor()
    existing_companies = cur.execute(query);

    con.close()

    pass


def appInfoToDb(obj):
    if isinstance(obj, dict):
        # check for db file, append
        con = getAppDbConnection()
        cur = con.cursor()

        # if the "jobs" table doesn't exist, create it
        if not tableExists("applications"):
            initJobsTableDB()

        companyRes = cur.execute(
            "SELECT company_id FROM companies WHERE workday_prefix=?",
            company_prefix)
        companyId = companyRes.fetchone()

        # table exists, insert a row
        res = cur.execute("INSERT INTO applications VALUES(?, ?, ?, ?, now(), now());",
                          obj["job_repid"], companyId, obj["title"], appStatusToInt(obj["status"]))

        res.commit()

        con.close()
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
        clickFilter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-automation-id='click_filter']"))
        )
        submitButton = driver.find_element(By.CSS_SELECTOR,
                                           "button[type='submit']")

        print("Login page buttons:")
        print(emailBox)
        print(pwBox)
        print(clickFilter)
        print(submitButton)

        emailBox.send_keys("kdillo893@gmail.com")
        pwBox.send_keys("SECRET PASSWORD")
        # TODO: for some reason the button is inactive for a few seconds
        print(clickFilter.is_enabled())
        clickFilter.click()
        print(submitButton.is_enabled())
        submitButton.send_keys(Keys.ENTER)
        submitButton.send_keys(Keys.RETURN)
    else:
        print('bad thing')
        return

    # how to guarantee this is a button?
    # submit_button.click()

    # check the "candidate home" by navigating
    candidateHome = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "[data-automation-id='navigationItem-Candidate Home']"))
    )

    print("Logged in, trying to reach candidate home")
    candidateHome.click()

    # read info on the row, send that to "write db" function
    jobsTable = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "[data-automation-id='applicationsSectionHeading']"))
    )

    print("At Candidate Home, trying to parse information about jobs")

    # Grab each <tr> with attribute data-automation-id="taskListRow"
    # TODO

    yield {"job_repid": "R12345", "company": "Discover", "title": "SoftDev", "status": "Pending", "applied": 2024-11-22, "updated": 2024-11-22}


if __name__ == '__main__':
    # TODO: have parms with pw store...
    applications = [
        {"job_repid": "R12345", "company": "Discover", "title": "SoftDev",
            "status": "Pending", "applied": 2024-11-22, "updated": 2024-11-22},
        {"job_repid": "R54321", "company": "FakeCompany", "title": "SoftDev",
            "status": "Pending", "applied": 2024-11-22, "updated": 2024-11-22},
    ]

    if False:
        driver = webdriver.Chrome()

        wdayLogins = [
            {"company": "Discover", "wday_prefix": "discover", "wd_ver": "wd5",
                "email": "kdillo893@gmail.com", "password": "TestPassword123"}
        ]

        for entry in wdayLogins:
            applications.push(checkWorkdayApps(
                driver, 'discover', 'wd5', None))

        driver.quit()

    writeApplicationsToDb(applications)
