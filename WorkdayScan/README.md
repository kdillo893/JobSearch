# Workday scanner
CURRENTLY WIP.
Workday is a popular tool used as a third-party job candidate tracking application for many companies.

This tool will use a set of credentials (stored in a simplified password manager)
for logging into job portal accounts using Selenium and scanning the application status
of the provided accounts.

# Progress to make:
1. Get data store correct
2. "Finish grabbing active/inactive applications from page"
  * Could look into cookie/credential/session saving and shoot off API requests
    to minimalize data usage or latency; would need to read around workday
3. Determine how to fetch credentials from password manager storage
  * Limit scope for that access and verify authenticity of site before write-to operation
  * either that or just bypass this and have manual-entry pause in script


## Building
I'm using pipenv to make python virtual environment management easier.

```
pipenv install
```

``pipenv shell`` to enter that venv.

If not using pipenv, can make your own venv for separation of duties.

```
python -m venv /path/to/virtual/env
source /path/to/virtual/env/bin/activate
pip install -r ./requirements.txt
```

Dont' forget to ``deactivate`` when you don't want to be in the virtual environment <3

## Running
```
./executableName /path/to/CredsSecretStore
```

## NOTES
### How I want it to work:
Basics is "take credentials and workday domain, login, check candidate home, check
active/inactive role tabs, populate output file by appending the information contained in those tables."

### How it should run (TDD focus):
#### Selenium navs
* For selenium page nav "mock", copying the HTML and button js, add to 
    /etc/hosts that has that domain subset redirect to localhost.
```
"Can open url at \[ns\].\[wd#\].workdayjobs.com" - yes, need "option provided"
"Navigate to Login"
"Enter login information and click login/Submit"
"After login, navigate to Candidate Home"
"On Candidate Home, read rows on Active tab and Inactive tab (all are visible)"
```
#### Creds 
```
"Pull list of credentials from file which includes wd namespace/url, email, pw"
```
Reaches:
```
"Have file cryptographically secure at rest (for now just load to mem)"
"
```

### How am I saving things?
Put the read information into a sqlite file. The pkey combo... not sure, need to think about what's there:

Tables that I'm thinking about:

companies
| ColumnName | Type | Nullable | Key/Relation | Added info |
| --------------- | --------------- | --------------- | -- | |
| company_id | long | NOT NULL | Unique, PKEY |              |
| company_name | text/varchar | NOT NULL |  |            |
| workday_url | varchar(128) | NOT NULL | |                  |
| careers_url | varchar(255) | NULLABLE | |                  |
| ... | ... | ... | |

applications
| ColumnName | Type | Nullable | Relation | AddedInfo |
| --------------- | --------------- | --------------- | --------------- | --------------- |
| job_reqid | varchar(10) | NOT NULL | -- | Whatever their board uses as IDs for the job |
| company_id | long | NOT NULL | FKEY(company) | this plus job_reqid should be unique |
| title | varchar(80) | NOT NULL | -- | Job title |
| status | BIT(2) | NOT NULL | -- | 4 states: applied = 0, rejected/not consideration = 1, processing = 2, ... = 3 |
| applied | datetime | NOT NULL | -- | time of application |
| updated | datetime | NOT NULL | -- | the time of the last change |

company_reps? (not sure if I want)
| ColumnName | Type | Nullable | Relation | AddedInfo |
| --------------- | --------------- | --------------- | --------------- | --------------- |
| company_id | long | NOT NULL | FKEY(company) | company they work for |
| name | varchar(100) | NOT NULL | -- | who are they |
| job_reqid | varchar(10) | NULLABLE | -- | what job did they contact me about? nullable|
| email | varchar(320) | NOT NULL | -- | Whatever their board uses as IDs for the job |


### Future ideas
ICIMS is also popular. Add that first.

Could extend this to generic URL, but would need
specific parsing for given application tracking systems.
