from ResumeClass import Resume

fileToRead = "TestResume.csv"

myResume = Resume(fileToRead)

print("basic info is", myResume.getBasicInfo())

print("education info is", myResume.getEduInfo())

print("Here is the lsit of jobs I have: ", myResume.getPrevJobs())

# for i in prevJobList:
#     i.ReturnAllJobData()