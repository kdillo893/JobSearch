# How am I doing these parts?

## Parsing data for storage


## Data storage for components to include in resume
Larger sections are the following:
* Skills
    * Simple set table, skill uniqueId, altSkill as different phrasing for the same
* Certifications
    * cert_id, certifier, certification_name, start_date, end_date, description
* Education
    * school_name, degree[varchar], degree_level[Enum(hs, bs, ba, ms, phd, md, dds, etc...)], enroll_date, grad_date,
    * coursework sub-table, like skills as a set
* Work Experience
    * job_id, employer, title, start_date, end_date, description?
    * job duties sub-table, set
    * notable tasks sub-table, set
* Projects
    * project, name, start_date, end_date, description
    * skills/tools used subtable?
* Hobbies & Interests
    * simple set list
* (Summary)
    * just store string somewhere to pull from. 
        Make a text file with a line per version, the line# is the version to use.

### Translate from raw to table or table to resume description?

## Defining components to include in building resume
Summary should be something I define myself... I think auto-generating is useless.
* Text file, each line-break is a new description to decide from.
* Generating new summary appends line to file, editing modifies the line

Most past working experience should be included.
* select from tasks and sub-duties the top # depending on keyword match.
    * keyword match is just hashmap of the line
* should select more from roles that contain more keyword matches.

Skills section should be highly correlative to the job description
* Correlation function for skill to job description lines

### Job Description parser:
thinking

Output of this would just be array of keyword sets (index per line).
Remove from keyword set any words that aren't 

### Component matching:
Thread per segment for matching; shared memory of constant set for keywords 
in the job description to match.


## Exporting/Building a document (docx?)

