# Tracking sheet updating tool
I have a simple google sheet for remotely viewable version of application tracking.
I want to push information

*NOTE, NOT CURRENTLY ADAPTABLE TO OTHER SPREADSHEETS*

## Pre-requisites
For the spreadsheet pipeline, would need to change the spreadsheetId within ``SheetsQuickstart.java``.

Also in order to access Google Sheets, you need a proper ``credentials.json`` with client/secret for the app
from google developer suite. This can be found at the link below:

[Google Cloud Sheets API credentials dashboard](https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials)

## Build

This app uses gradle. To build, run the following in the current directory:

```
./gradlew build
```

## Running

Run with gradlew after building.

```
cd TrackingSheet
./gradlew run
```

On the first run, the CLI will ask to follow along to complete authorization
and store a credential.
The stored credentials currently have a timeout issue and need manual clearing,
which needs addressing.
