from JobApplicationClass import JobApplication, JobAppList
from datetime import datetime
# import csv

#self,CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink
NewJob = JobApplication(-1,"Among Us", "Impsoster", datetime.strptime("2-5-2025","%m-%d-%Y"),"N/A",False)

newJobDate = NewJob.GetApplyDate()
print(newJobDate.year, newJobDate.month, newJobDate.day)

NEOjobAppList = JobAppList("JobApplicationsTest.csv")

print("my list of applied jobs is: ", NEOjobAppList.getJobListasStr())


#prints out all files read in, use for debugging
# for curJA in jobApplicationList:
#     print(curJA.GetEverything())


