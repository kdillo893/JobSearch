# Job searching and application tools

Basic things to receive info about my job applications and track them.

An idea would be to assist the "application filling out" stuff and 
the "looking for reasonable jobs" part across existing sites, but I believe
many of the big sites and career pages for specific companies have restrictions
on bots or programs.

## Pre-requisites
*NOTE, NOT CURRENTLY ADAPTABLE TO OTHER SPREADSHEETS*
For the spreadsheet pipeline, would need to change the spreadsheetId within ``SheetsQuickstart.java``.

Also in order to access Google Sheets, you need a proper ``credentials.json`` with client/secret for the app
from google developer suite. This can be found at the link below:

[Google Cloud Sheets API credentials dashboard](https://console.cloud.google.com/apis/api/sheets.googleapis.com/credentials)

## Build

I use gradle in this. To build, move into the ``TrackingSheet`` directory and build like below:

```
cd TrackingSheet
./gradlew build

```

## Running
*NOTE, NOT CURRENTLY ADAPTABLE TO OTHER SPREADSHEETS*

Run with gradlew after building.

```
cd TrackingSheet
./gradlew run
```
