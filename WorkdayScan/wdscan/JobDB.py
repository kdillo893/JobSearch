from enum import Enum

import sqlite3

# classes, types, and cache structures


class DatabaseConfig:
    """
    Singleton for db configuration instance to hold db connection info
    """

    _db_file: str | None = None

    def __init__(self, db_file=None):
        if db_file is None:
            # for now, just make this default:
            db_file = "jobapps.db"

        DatabaseConfig._db_file = "jobapps.db"

    @staticmethod
    def getDbFile() -> str | None:
        return DatabaseConfig._db_file


class OpenConnection:
    """
    Class for chaining unresolved connections to sqlite,
    which allows stacking statements for a single transaction
    without explicit open/close.
    """

    _sqliteConnection: sqlite3.Connection | None = None

    # add to list by query executed and the result of execution
    executionResults: list[dict[str, tuple]] = None

    def __init__(self):

        self._sqliteConnection = sqlite3.connect(DatabaseConfig.getDbFile())

    def commitAndClose(self):
        self._sqliteConnection.commit()
        self._sqliteConnection.close()
        pass


type ResultsList = list[dict[str, str]]


_companyIdCache = {}


def clearCompanyIdCache():
    global _companyIdCache
    _companyIdCache = {}

# Fake class for showing the table definitions


class applications:
    job_reqid: str   # pkey part1, not null
    company_id: int  # pkey part2, not null
    title: str
    status: int
    applied: int  # date
    update: int   # date


class companies:
    company_id: int  # pkey 1, not null
    company_name: str
    workday_prefix: str
    company_path: str
    careers_url: str


# Data fixing queries


def initJobsDbFile():
    print("No .db file, creating it with connect")

    # companies table
    companiesTableCreateQuery = """CREATE TABLE IF NOT EXISTS
            companies(company_id NOT NULL, company_name, workday_prefix,
                    careers_url);
        """

    # applications table
    applicationsTableCreateQuery = """CREATE TABLE IF NOT EXISTS
            applications(job_reqid NOT NULL, company_id NOT NULL,
            title, status, applied, updated, unique(job_reqid, company_id));
        """

    con = sqlite3.connect(DatabaseConfig.getDbFile())
    print(con.autocommit)

    cursor = con.cursor()

    cursor.execute(companiesTableCreateQuery)
    cursor.execute(applicationsTableCreateQuery)

    con.commit()

    # how do I check if they're created properly?


# Basic execution queries

def executeQuery(query, data: tuple | dict = None) -> ResultsList:
    '''
    Given the sqlite db filename, attempt to open a connection and execute a
    single query with multiple results.
    Returns None if didn't execute properly or desired array of results
    '''
    res = None

    con = sqlite3.connect(DatabaseConfig.getDbFile())
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


def executeQuerySingle(query, data: tuple = None):
    '''
    Given the sqlite db filename, attempt to open a connecta
    query returning a single result.
    Returns None if the query didn't execute properly or desired single result
    '''
    res = None

    con = sqlite3.connect(DatabaseConfig.getDbFile())
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


def executeStatementWithConnection(connection: OpenConnection,
                                   query,
                                   data: tuple = None):
    """
    Using an open connection, execute statement and postpone commit.
    If there are results (ie insert and ID needs recording), OpenConnection
    object will store the list of results from each execution
    """

    con = sqlite3.connect(DatabaseConfig.getDbFile())
    cursor = con.cursor()
    try:
        if data is None:
            cursor.execute(query).fetchone()
        else:
            cursor.execute(query, data).fetchone()
    except sqlite3.Error:
        pass

    return


def tableExists(tableName):
    res = executeQuerySingle(
        "SELECT name FROM sqlite_schema WHERE tbl_name = \"applications\""
    )

    if res is None:
        return False

    name = res[0]
    print(name)
    if (name == tableName):
        return True

    return False


# Translate app status as enum
class AppStatus(Enum):
    Pending = 0
    NotSelected = 1
    Submitted = 2
    NotSubmitted = 3
    Removed = 4
    Other = 5


def getAppStatusFromString(statusString) -> AppStatus:
    if statusString in ["No Longer Under Consideration", "Not Selected"]:
        return AppStatus.NotSelected
    elif statusString == "Pending":
        return AppStatus.Pending
    elif statusString == "Not Submitted":
        return AppStatus.NotSubmitted
    elif statusString == "Submitted":
        return AppStatus.Submitted
    else:
        return AppStatus.Other
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


# Common Queries

def getExistingJobApps(apps):
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
    existingJobApps = executeQuery(query)


def getCompanyIdFromName(companyName):
    """
    Search company name cache for ID, and if not in cache query db for the ID
    associated with the name of a company.
    """
    global _companyIdCache

    if companyName in _companyIdCache:
        return _companyIdCache[companyName]

    res = getCompanyIdByName(companyName)

    if res and len(res) > 0:
        companyId = res[0]
        _companyIdCache[companyId]
        print(f"added [{companyName}:{companyId}] to companyIdCache")

    # none found, return none
    return None


def getCompanyIdByName(companyName):
    companyIdQuery = "SELECT company_id FROM companies WHERE company_name = ?"
    return executeQuerySingle(companyIdQuery, [companyName])
