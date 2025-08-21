import time
import os
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from JobDB import initJobsDbFile, executeQuery, \
    executeQuerySingle, getAppStatusFromString, getExistingJobApps, \
    DatabaseConfig


logger = logging.getLogger(__name__)


def isEntryInExistingApps(app, existingApps):
    return True


def writeApplicationsToDb(apps):
    """
    Begin to fire off writes of application info to database
    """

    print("Checking job applications table in sqlite file...")

    # with the array "apps", construct the sql statement for adding
    # 1. get db entries that match job_reqid and company_id of "apps" elements
    existingApps = getExistingJobApps(apps)
    print(existingApps)

    appsToAdd = filter(
        lambda app: isEntryInExistingApps(app, existingApps), apps)

    print("Writing new job applications to db...")
    for app in appsToAdd:
        writeJobappInfoToDb(app)

    pass


def writeJobappInfoToDb(jobApp):
    """
    append application using related company and application info
    """

    if isinstance(jobApp, dict):
        companyName = jobApp['company']

        prefixQuery = "SELECT company_id FROM companies WHERE company = ?;"
        companyRes = executeQuerySingle(prefixQuery, company_prefix)
        companyId = companyRes.fetchone()

        if not companyId:
            # create one with name, put in cache
            
            pass

        insertQuery = "INSERT INTO applications VALUES(?, ?, ?, ?, now(), now());"
        # table exists, insert a row
        res = executeQuery(insertQuery,
                           (jobApp["job_repid"],
                            companyId,
                            jobApp["title"],
                            getAppStatusFromString(jobApp["status"]))
                           )

        return res

    pass


def fetchWorkdayJobAppsPerCompany(driver: webdriver.Chrome,
                                  company: str,
                                  wdver: str,
                                  companyPath: str,
                                  creds):
    """
    Utilizing Selenium WebDriver, fetch application info from workday site
    """

    url = f'https://{company}.{wdver}.myworkdayjobs.com/en-US/{companyPath}/userHome'
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

        # for some reason the button is inactive for a few seconds
        time.sleep(1)
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
    # TODO: parse table for rows, chunk out data from its text,
    #   use yield to return object rows piecewise

    yield {"job_repid": "R12345", "company": "Discover",
           "title": "SoftDev", "status": "Pending",
           "applied": 2024-11-22, "updated": 2024-11-22}
    return


if __name__ == '__main__':
    # logging config
    logging.basicConfig(filename="wdscan_app.log", level=logging.INFO)

    # TODO: have parms with pw store file details

    # example of needed info per row
    company_prefix = "discover"
    wd_ver = "wd5"
    company_path = "Discover"

    if (company_prefix is None or company_prefix == ""
            or wd_ver is None or wd_ver == ""):
        exit(-1)

    # example applications
    applications = [
        {"job_repid": "R12345", "company": "Discover", "title": "SoftDev",
            "status": "Pending", "applied": 2024-11-22, "updated": 2024-11-22},
        {"job_repid": "R54321", "company": "FakeCompany", "title": "SoftDev",
            "status": "Pending", "applied": 2024-11-22, "updated": 2024-11-22},
    ]

    # TODO: troubleshoot webdriver fetch
    if False:
        driver = webdriver.Chrome()

        wdayLogins = [
            {"company": "Discover", "wday_prefix": "discover",
                "wd_ver": "wd5", "wd_companyPath": "Discover",
                "email": "kdillo893@gmail.com", "password": "TestPassword123"}
        ]

        for entry in wdayLogins:
            applications.push(fetchWorkdayJobAppsPerCompany(
                driver, 'discover', 'wd5', None))

        driver.quit()

    # Temporary: log to file
    logging.info(f'applicationInfo={applications}')

    # Database stuff

    DatabaseConfig("jobapps.db")
    if not os.path.isfile(DatabaseConfig.getDbFile()):
        # create basic tables
        initJobsDbFile()

    writeApplicationsToDb(applications)
