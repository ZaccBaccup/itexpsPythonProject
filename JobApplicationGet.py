from JobApplicationClass import JobApplication

#self,CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink
NewJob = JobApplication("Among Us", "Impsoster", 2,5,2025,"N/A")

newJobDate = NewJob.GetApplyDate()
print(newJobDate.year, newJobDate.month, newJobDate.day)