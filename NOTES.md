# Job Searching Tools

My personal things to make job searching on the web easier.


Currently only have something to add row to my JobSearches tracking sheet on
Google Sheets. In process of creating a pipeline to parse "my applications" and 
send those new rows to my spreadsheet.

Later would have a mechanism for querying if that title and posting matches an existing
row and update the status of that row in my spreadsheet.

This would probably be much easier as a database and some custom UI instead...

Researching, found "competitive" solution in "Simplify":
[Simplify: Job Searching and Tracking](https://simplify.jobs/)

## Goals
0. Resume Tailoring:
  * Have an info-base of things I would put on the resume, select subsets depending on match to JD (keywords 100% include, rough match include above certain thresholds, etc)
1. Take information from applications (browser extension or email responses specifically from career sites) 
  * "title", "Date", "Accept/Reject/Applied" etc, "company", "location", "link" for how to view posting and process...
2. Post to my "JobSearch" google sheet on the "2024 Searches" page, appending rows at the bottom with above data.
  * testing phase would just supply current time and a counter for some row with garbage data.
3. link those pieces together and have a cronjob on my Raspberry Pi to pull, filter, and append for my sheet.
  * (alternative is just a hook for received email filter, would need to have connection logic)

### 0. Resume Tailoring:
Many sites have this as a paid option. I can probably do this myself after looking into the structure of .docx, and I could export that to .pdf using other software.
1. Info base of "Me" for resume
  * SQLite file, tables for different sections
2. "ease of editing" desktop ui for this database:
  * Graphics APIs (OpenGL, Mesa, GLES, GLX/WGL, EGL/GLUT, fglrx/Catalyst)
  * DRI/DRM (Direct Rendering Infrastructure/Manager)
  * X Window System
  * Cairo/Pixman
  * Compositor
  * Wayland
  * Qt
  * Gtk = GIMP Toolkit
  * .Net stuff for windows... MAUI

### 1. "Listening" for my applications
What's the most effective way to do this?
1. Browser extension
  * would need to tune this for sites...
  * would only be available on machines I install the extension...
  * maintaining would suck.
  * only have intro knowledge for chrome extensions, would need to do more for FF...
  * not quick to implement.
2. Email parsing
  * What if an application doesn't send an email?
  * Could be VERY scary for security if this starts targeting emails I don't want...
3. Selenium script to parse information from the actual job board on a regular schedule
  * requires consistent internet connection for tool to work.
  * Definitely uses too much excess bandwidth compared to other ways
    * Could do something crazy like block CDNs and CSS so that images don't load
    and content is mostly static... every fucking web thing runs on JavaScript
    so I can't really block that to reduce bandwidth

## Problems with job searching
There are a couple problems with the current job board environment that I've
become familiar with over the past several months.

1. Connection is king, and if you're not currently connected, you need to be
making initial connections to people across the industry fairly regularly.
2. Job listings are often gamed to the point of certain companies re-appearing
or posting the same opening for various locations.
3. Because of the presence of multiple different career sites and boards, 
it's often hard to find all the openings that are relevant OR postings 
are repeated across sites.
4. There are often listings that are multiple months old or lead to positions 
that never get proper replies when drilling into the employer's system.
5. Applying manually sucks, and most of the time the forms are nearly identical.
6. I am absolutely terrible at professional networking, immersing myself in
professional networking spaces, and I'm bad at selling my skills and talents.
7. I hate needing to type stuff in to a spreadsheet each time I apply, and 
I often forget where I've applied or when to check back.

## Ideas for solutions to my problems
The problems that I can think of solutions for immediately are to
narrow the searches or track places that I've applied to in a better way than
spreadsheets. The next obvious is to make applying much easier than typing.

### Application tracking idea (2, 3, 7) 
Google sheets api stuff, maybe a chrome extension that pulls info
from the page on the listing and pings the sheets api with that data.
Auto-timing based on when I ping the sheet, highlight difference from date.now

### Speeding up individual application time (5)
One way to track would be "time myself manually, then make a selenium script
for common HR pages to auto-fill with my resume info with a pause to check"

### Searching across multiple career sites at once and aggregating (3, 4)
This would involve seeing if there's an API available for each of the popular
boards and coding up a thing to pull from each, organize them into a common
data pattern, and purge duplicates.
