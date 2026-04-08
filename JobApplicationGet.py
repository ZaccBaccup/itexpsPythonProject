from JobApplicationClass import JobApplication
import csv

#self,CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink
NewJob = JobApplication("Among Us", "Impsoster", 2,5,2025,"N/A")

newJobDate = NewJob.GetApplyDate()
print(newJobDate.year, newJobDate.month, newJobDate.day)


fileToRead = "TestOutputJobs.csv"

jobApplicationList = []

print("Reading from file", fileToRead, "utilizing the csv library...")
with open(fileToRead, 'r') as csvfile:
    csvreader = csv.reader(csvfile)  # Reader object
    next(csvreader) #to add consistency, the column names are the first row.
    for curRow in csvreader:#adds the row into a JobApplication Object
        try:
            jobApplicationList.append(JobApplication(curRow[0], curRow[1],int(curRow[2]), int(curRow[3]),int(curRow[4]), curRow[5]))
        except IndexError:
            print("Uh oh! This job application only has", len(curRow), "entries when it should have 6!")



for curJA in jobApplicationList:
    print(curJA.GetEverything())


