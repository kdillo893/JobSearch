from enum import Enum
import errno
import os

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

    # add query string and results of execution to list
    executionResults: list[dict[str, tuple]] | None = None

    def __init__(self):
        dbFile = DatabaseConfig.getDbFile()
        if dbFile is None:

            return

        self._sqliteConnection = sqlite3.connect(dbFile)

    def commitAndClose(self):
        if self._sqliteConnection is None:
            return

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
    company_path: str # path string workday, eg {prefix}.{baseUrl}/company_path
    careers_url: str


# Data fixing queries


def initJobsDbFile():
    print("No .db file, creating it with connect")

    # companies table
    companiesTableCreateQuery = """CREATE TABLE IF NOT EXISTS
            companies(company_id NOT NULL, company_name, workday_prefix,
            company_path, careers_url);
        """

    # applications table
    applicationsTableCreateQuery = """CREATE TABLE IF NOT EXISTS
            applications(job_reqid NOT NULL, company_id NOT NULL,
            title, status, applied, updated, unique(job_reqid, company_id));
        """

    dbFile = DatabaseConfig.getDbFile();
    if dbFile is None:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "NoDbFileProvided")

    con = sqlite3.connect(dbFile)
    print(con.autocommit)

    cursor = con.cursor()

    cursor.execute(companiesTableCreateQuery)
    cursor.execute(applicationsTableCreateQuery)

    con.commit()

    # how do I check if they're created properly?


# Basic execution queries

def executeQuery(query, data: tuple | dict | None = None) -> ResultsList:
    '''
    Given the sqlite db filename, attempt to open a connection and execute a
    single query with multiple results.
    Returns None if didn't execute properly or desired array of results
    '''
    res = None
    dbFile = DatabaseConfig.getDbFile()
    if dbFile is None:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "NoDbFileProvided")

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


def executeQuerySingle(query, data: tuple | None = None):
    '''
    Given the sqlite db filename, attempt to open a connecta
    query returning a single result.
    Returns None if the query didn't execute properly or desired single result
    '''
    res = None

    dbFile = DatabaseConfig.getDbFile()
    if dbFile is None:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "NoDbFileProvided")

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


#todo, operate off oopening connections to the db instance so I don't need to 
#   do the "connect" operation each time...
def executeStatementWithConnection(connection: OpenConnection,
                                   query,
                                   data: tuple | None = None):
    """
    Using an open connection, execute statement and postpone commit.
    If there are results (ie insert and ID needs recording), OpenConnection
    object will store the list of results from each execution
    """

    dbFile = DatabaseConfig.getDbFile()
    if dbFile is None:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "NoDbFileProvided")

    con = sqlite3.connect(dbFile)
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
    """
    Based on the input array @apps with job id and company id, search for
    entries in the applications table with matching ID and return the entry
    with the unique IDs.
    ... this seems useless.
    """
    # whereString = ""
    # if len(apps) > 0:
    #     whereString = " WHERE "
    #
    # appsQueryClauses = [f"""job_reqid = \"{a["job_repid"]}\"
    #                     AND company_id = \"{getCompanyIdFromName(a["company"])}\""""
    #                     for a in apps]
    # whereClauses = " OR ".join(appsQueryClauses)

    query = """SELECT job_reqid, company_id FROM applications;"""
    # query = """SELECT job_reqid, company_id FROM applications {} {};"""\
    # .format(
    #     whereString,
    #     whereClauses)

    print(query)

    # validating the statement
    print(sqlite3.complete_statement(query))

    # 2. query filter out the from the apps list anything in the matched query
    existingJobApps = executeQuery(query)

    return existingJobApps


def insertCompany(companyName, workdayPrefix, companyPath, careersUrl):
    """
    Insert a new company into the companies table, returning the new ID
    """

    # do a single select to get the highest company id, then increment.
    # this should need locking in the future or "cross process" communication
    # if it's not just this program running.
    getLargestCompanyIdQuery = """SELECT MAX(company_id) FROM companies;"""
    companyIdRes = executeQuerySingle(getLargestCompanyIdQuery)
    companyId = 1
    if companyIdRes and len(companyIdRes) > 0:
        #could be either faulty execution OR no entries...
        returnId = companyIdRes[0]
        if returnId is not None:
            companyId = int(companyIdRes[0]) + 1


    insertCompanyQuery = """INSERT INTO companies(company_id, company_name, workday_prefix,
                    company_path, careers_url)
                    VALUES(?, ?, ?, ?, ?) RETURNING company_id;"""

    res = executeQuerySingle(insertCompanyQuery,
                             (companyId, companyName, workdayPrefix,
                              companyPath, careersUrl)
                             )

    if res and len(res) > 0:
        companyId = res[0]
        _companyIdCache[companyName] = companyId
        print(f"added [{companyName}:{companyId}] to companyIdCache")
        return companyId

    return None


def insertApplication(jobApp, companyId):
    """
    Insert new job app entry into applications table, return the ID
    """

    insertQuery = "INSERT INTO applications VALUES(?, ?, ?, ?, date('now'), date('now'));"

    # table exists, insert a row
    res = executeQuery(insertQuery,
                       (jobApp["job_repid"],
                        companyId,
                        jobApp["title"],
                        getAppStatusFromString(jobApp["status"]).value)
                       )

    if res and len(res) > 0:
        #applicationId = res[0]
        #print(f"added application [{job_repid}] to db")
        return res

    return None


def getCompanyIdFromName(companyName):
    """
    Search company name cache for ID, and if not in cache query db for the ID
    associated with the name of a company.
    """
    global _companyIdCache

    if companyName in _companyIdCache:
        return _companyIdCache[companyName]

    print("querying for " + companyName)
    res = queryCompanyIdByName(companyName)

    if res and len(res) > 0:
        companyId = res[0]
        _companyIdCache[companyId]
        print(f"added [{companyName}:{companyId}] to companyIdCache")

    # none found, return none
    return None


def queryCompanyIdByName(companyName):
    companyIdQuery = "SELECT company_id FROM companies WHERE company_name = ?"
    return executeQuerySingle(companyIdQuery, (companyName, ))
