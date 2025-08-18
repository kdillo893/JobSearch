from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import sqlite3

import time

company_prefix = "discover"
wd_ver = "wd5"
DB_FILE = "applications.db"

if (company_prefix is None or company_prefix == ""
        or wd_ver is None or wd_ver == ""):
    exit(-1)


# CompanyID to name/workday-prefix mapping, avoid repeated queries
companyIdCache = {}

type ResultsList = list[dict[str, str]]


def executeQuery(dbFile, query, data=None) -> ResultsList:
    '''
    Given the sqlite db filename, attempt to open a connection and execute the
    query. Straightforward query without parameters.
    Returns None if the query didn't execute properly or the array of results
    '''
    res = None

    con = sqlite3.connect(dbFile)
    cursor = con.cursor()

    try:
        if data is None:
            res = cursor.execute(query).fetchall()
        else:
            res = cursor.execute(query, data).fetchall()
        con.commit()
    finally:
        # catch doesn't matter, we just want to ensure closure.
        cursor.close()
        con.close()

    return res


def executeQuerySingle(dbFile, query, data=None):
    '''
    Given the sqlite db filename, attempt to open a connection and execute the
    query. Straightforward query without parameters.
    Returns None if the query didn't execute properly or the single result
    '''
    res = None

    con = sqlite3.connect(dbFile)
    cursor = con.cursor()

    try:
        if data is None:
            res = cursor.execute(query).fetchone()
        else:
            res = cursor.execute(query, data).fetchone()
        con.commit()
    finally:
        # catch doesn't matter, we just want to ensure closure.
        cursor.close()
        con.close()

    return res


def tableExists(tableName):
    res = executeQuerySingle(
        DB_FILE,
        "SELECT name FROM sqlite_schema WHERE tbl_name = \"applications\""
    )

    if res is None:
        return False

    name = res[0]
    print(name)
    if (name == tableName):
        return True

    return False


def initJobsTableDB():
    print("No applications.db file, creating it...")

    # companies table
    res = executeQuery(DB_FILE, """CREATE TABLE IF NOT EXISTS
                companies(company_id NOT NULL, company_name, workday_prefix,
                        careers_url);
            """)

    if res is None:
        print("ERROR creating companies table")

    # applications table
    res = executeQuery(DB_FILE, """CREATE TABLE IF NOT EXISTS
                applications(job_reqid, company_id, title, status,
                        applied, updated, unique(job_reqid, company_id));
            """)
    if res is None:
        print("ERROR creating applications table")

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
    """
    Begin to fire off writes of application info to database
    """

    print("Checking job applications table in sqlite file...")

    # Check if the table exists first:
    if not tableExists("applications"):
        initJobsTableDB()
        print("applications table created...")

    # with the array "apps", construct the sql statement for adding
    # 1. get db entries that match job_reqid and company_id of "apps" elements

    query = f"""SELECT job_reqid, company_id
        FROM applications WHERE 
          {" OR ".join(
           [f"""job_reqid = \"{a["job_repid"]}\"
                AND company_id = \"{getCompanyIdFromName(a["company"])}\""""
            for a in apps])
           }
        ;"""
    print(query)

    # validating the statement
    print(sqlite3.complete_statement(query))

    # 2. query filter out the from the apps list anything in the matched query
    existing_companies = executeQuery(DB_FILE, query)

    print("Writing new job applications to db...")
    # TODO: incomplete

    pass


def getCompanyIdFromName(companyName):
    """
    Search company name cache for ID, and if not in cache query db for the ID
    associated with the name of a company.
    """

    if companyName in companyIdCache:
        return companyIdCache[companyName]

    companyIdQuery = "SELECT company_id FROM companies WHERE company_name = ?"
    res = executeQuerySingle(DB_FILE,
                             companyIdQuery,
                             (companyName,))

    if res and len(res) > 0:
        companyId = res[0]
        companyIdCache[companyId]
        print(f"added [{companyName}:{companyId}] to companyIdCache")

    # none found, return none
    return None


def appInfoToDb(obj):
    """
    append application using related company and application info
    """

    if isinstance(obj, dict):

        # TODO: next commit will do this check once rather than repeatedly.
        # if the "jobs" table doesn't exist, create it
        if not tableExists("applications"):
            initJobsTableDB()

        prefixQuery = "SELECT company_id FROM companies WHERE workday_prefix=?;"
        companyRes = executeQuerySingle(DB_FILE, prefixQuery, company_prefix)
        companyId = companyRes.fetchone()

        if not companyId:
            # create one with
            pass

        insertQuery = "INSERT INTO applications VALUES(?, ?, ?, ?, now(), now());"
        # table exists, insert a row
        res = executeQuery(DB_FILE,
                           insertQuery,
                           (obj["job_repid"],
                            companyId,
                            obj["title"],
                            appStatusToInt(obj["status"]))
                           )

        return res

    pass


def checkWorkdayApps(driver: webdriver.Chrome,
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

        time.sleep(1)
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
    # TODO: parse table for rows, chunk out data from its text

    yield {"job_repid": "R12345", "company": "Discover",
           "title": "SoftDev", "status": "Pending",
           "applied": 2024-11-22, "updated": 2024-11-22}


if __name__ == '__main__':
    # TODO: have parms with pw store file details

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
