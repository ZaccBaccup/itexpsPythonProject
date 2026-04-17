class Resume:

    def __init__(self, basicInfoList,eduInfoList,prevJobList):
        self.__name = basicInfoList[0]
        self.__jobTitle = basicInfoList[1]
        self.__location = basicInfoList[2]
        self.__highestEdu = eduInfoList
        self.__prevJobs = prevJobList


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