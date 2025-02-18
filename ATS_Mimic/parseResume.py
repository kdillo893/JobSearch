import pypdf

reader = pypdf.PdfReader("/home/kdill/Documents/Work/JobApplicationStuff/Kevin_Dillon_resume.pdf")
print(reader.pages[0].extract_text(extraction_mode="layout"))
