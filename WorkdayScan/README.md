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

