# Workday scanner
Workday is a popular tool used as a third-party job candidate tracking application for many companies.

This tool will use a set of credentials (stored in a simplified password manager)
for logging into job portal accounts using Selenium and scanning the application status
of the provided accounts.

## Building
It'll probably just be a python script to make things easy; would need env that
includes the python selenium library.

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
"Can open url at \[ns\].\[wd#\].workdayjobs.com"
"Navigate to Login"
"Enter login information and click login/Submit"
"After login, navigate to Candidate Home"
"On Candidate Home, read rows on Active tab"
"On Candidate Home, click Inactive tab and read rows"
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

### Future ideas
ICIMS is also popular. Add that first.

Could extend this to generic URL, but would need
specific parsing for given application tracking systems.
