# Job Searching Tools

My personal things to make job searching on the web easier.


## Goals
1. Take incoming emails from my gmail on kdillo893@gmail.com and check for
"applied" or "application", filter that data for
  * "title", "Date", "Accept/Reject/Applied" etc, "company", "location", "link" for how to view posting and process...
2. Post to my "JobSearch" google sheet on the "2024 Searches" page, appending rows at the bottom with above data.
  * testing phase would just supply current time and a counter for some row with garbage data.
3. link those pieces together and have a cronjob on my Raspberry Pi to pull, filter, and append for my sheet.
  * (alternative is just a hook for received email filter, would need to have connection logic)

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
