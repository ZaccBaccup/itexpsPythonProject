
#CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink
import csv


from datetime import datetime

class JobAppList:
    


    def __init__(self, fileToRead):
        self.__jobList = []

        print("Reading from file", fileToRead, "utilizing the csv library...")
        with open(fileToRead, 'r') as csvfile:
            csvreader = csv.reader(csvfile)  # Reader object
            next(csvreader) #to add consistency, the column names are the first row.
            for curRow in csvreader:#adds the row into a JobApplication Object
                try: #ID,companyName,jobTitle,appDay,appMonth,appYear,jobLink,isFollowedUp
                    self.__jobList.append(JobApplication(curRow[0], curRow[1],curRow[2], datetime.strptime(curRow[3],"%m-%d-%Y"),curRow[4],bool(int(curRow[5])))) #int(curRow[3]),int(curRow[4]), curRow[5],bool(int(curRow[6]))))
                except IndexError:
                    print("Uh oh! This job application only has", len(curRow), "entries when it should have 6!")
        

    def getJobList(self):
        return self.__jobList
    

    def getJobListasStr(self):
        strList = []
        for i in self.__jobList:
            strList.append(i.GetEverythingAsStr())

        return strList

class JobApplication:

    def __init__(self,ID,companyName,jobTitle,appDate,jobLink,isFollowedUp):
        self.__ID = ID
        self.__companyName = companyName
        self.__jobTitle = jobTitle
        self.__applyDate = appDate
        self.__jobLink = jobLink
        self.__isFollowedUp = isFollowedUp

    def GetApplyDate(self):
        return self.__applyDate
    
    def GetCompanyName(self):
        return self.__companyName
    
    def GetJobTitle(self):
        return self.__jobTitle

    def GetJobLink(self):
        return self.__jobLink
    
    def GetFollowedUpStatus(self):
        return self.__isFollowedUp
    
    def GetEverything(self):
        return [self.__ID, self.__companyName, self.__jobTitle, str(self.__applyDate.month)+"-"+str(self.__applyDate.day)+"-"+str(self.__applyDate.year), self.__jobLink, self.__isFollowedUp]
    
    def GetEverythingAsStr(self):
        return "Job Number "+  self.__ID + ": company Name: " + self.__companyName + ", title:" + self.__jobTitle + ", applied on:  " + str(self.__applyDate.month)+"-"+str(self.__applyDate.day)+"-"+str(self.__applyDate.year) + ", link is: ", self.__jobLink