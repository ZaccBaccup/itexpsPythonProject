import csv
from ResumeClass import Resume, PreviousJob

fileToRead = "TestResume.csv"

BasicInfo = []
eduInfo = []
prevJobList = []

print("Reading from file", fileToRead, "utilizing the csv library...")
with open(fileToRead, 'r') as csvfile:
    csvreader = csv.reader(csvfile)  # Reader object
    next(csvreader) #Ignore first row
    BasicInfo = next(csvreader)
    # print("the basic info is",BasicInfo)
    next(csvreader)
    eduInfo = next(csvreader)
    # print("the education info is",eduInfo)
    next(csvreader)

    for curRow in csvreader:
        prevJobList.append(PreviousJob(curRow))
    
# print()

# print("The first job is:",prevJobList[0].ReturnAllJobData())
# for i in prevJobList:
#     i.ReturnAllJobData()