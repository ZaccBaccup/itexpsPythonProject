from JobApplicationClass import JobApplication
from datetime import datetime
import csv

#self,CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink
NewJob = JobApplication(-1,"Among Us", "Impsoster", datetime.strptime("2-5-2025","%m-%d-%Y"),"N/A",False)

newJobDate = NewJob.GetApplyDate()
print(newJobDate.year, newJobDate.month, newJobDate.day)

fileToRead = "JobApplicationsTest.csv"

jobApplicationList = []

print("Reading from file", fileToRead, "utilizing the csv library...")
with open(fileToRead, 'r') as csvfile:
    csvreader = csv.reader(csvfile)  # Reader object
    next(csvreader) #to add consistency, the column names are the first row.
    for curRow in csvreader:#adds the row into a JobApplication Object
        try: #ID,companyName,jobTitle,appDay,appMonth,appYear,jobLink,isFollowedUp
            jobApplicationList.append(JobApplication(curRow[0], curRow[1],curRow[2], datetime.strptime(curRow[3],"%m-%d-%Y"),curRow[4],bool(int(curRow[5])))) #int(curRow[3]),int(curRow[4]), curRow[5],bool(int(curRow[6]))))
        except IndexError:
            print("Uh oh! This job application only has", len(curRow), "entries when it should have 6!")



#prints out all files read in, use for debugging
# for curJA in jobApplicationList:
#     print(curJA.GetEverything())


