import csv



class Resume:

    def __init__(self, fileToRead):

        basicInfo = []
        eduInfo = []
        prevJobList = []

        print("Reading from file", fileToRead, "utilizing the csv library...")
        with open(fileToRead, 'r') as csvfile:
            csvreader = csv.reader(csvfile)  # Reader object
            next(csvreader) #Ignore first row
            basicInfo = next(csvreader)
            # print("the basic info is",BasicInfo)
            next(csvreader)
            eduInfo = next(csvreader)
            # print("the education info is",eduInfo)
            next(csvreader)

            for curRow in csvreader:
                prevJobList.append(PreviousJob(curRow))

        self.__name = basicInfo[0]
        self.__jobTitle = basicInfo[1]
        self.__location = basicInfo[2]
        self.__collegeName = eduInfo[0]
        self.__degreeName = eduInfo[1]
        self.__collegeStart = eduInfo[2]
        self.__collegeEnd = eduInfo[3]
        self.__prevJobs = prevJobList

    # return list of strings representing basic information
    def getBasicInfo(self):
        return [self.__name,self.__jobTitle, self.__location]
    
    #return list of strings representing college accomplishments
    def getEduInfo(self):
        return [self.__collegeName, self.__degreeName, self.__collegeStart, self.__collegeEnd]
    
    #return list of previous jobs, including all their attributes
    def getPrevJobs(self):
        jobArray = []

        for i in self.__prevJobs:
            jobArray.append(i.ReturnAllJobData())
        return jobArray
    
    
    def PrintAllJobs(self):
        for i in self.__prevJobs:
            print(i.ReturnAllJobData())



class PreviousJob:
    def __init__(self,initList):
        try:
            self.__jobDuties = [] 
            # print("creating a previousjob instance with", initList)
            # print()
            self.__jobRole = initList.pop(0)
            self.__employer = initList.pop(0)
            self.__jobStart = int(initList.pop(0))
            self.__jobEnd = initList.pop(0)
        except IndexError:
            print("Uh oh! This job application only has", len(initList), "entries when it should have at least 4!")
        for i in initList:
            self.__jobDuties.append(i)
            # print("Adding ", i,"to object",self)
        
    def ReturnAllJobData(self):
        retString = ""
        retString+=self.__jobRole + ", " + self.__employer + ", " +str(self.__jobStart) + "-" + self.__jobEnd + ":"
        for curJob in self.__jobDuties:
            retString += curJob + ", "
        print(retString)
        return retString