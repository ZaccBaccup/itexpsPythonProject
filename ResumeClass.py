class Resume:
    name = ""
    jobTitle = ""
    location = ""

    highestEdu = []
    prevJobs = []
    def __init__(self, paramList):
        for curRow in paramList:
            pass



class PreviousJob:
    __jobRole = ""
    __employer = ""
    __jobStart = -999
    __jobEnd = ""
    __jobDuties = [] 
    def __init__(self,initList):
        try:
            print("creating a previousjob instance with", initList)
            print()
            self.__jobRole = initList.pop(0)
            self.__employer = initList.pop(0)
            self.__jobStart = int(initList.pop(0))
            self.__jobEnd = initList.pop(0)
        except IndexError:
            print("Uh oh! This job application only has", len(initList), "entries when it should have at least 4!")
        for i in initList:
            self.__jobDuties.append(i)
        
    def ReturnAllJobData(self):
        retString = ""
        retString+=self.__jobRole + ", " + self.__employer + ", " +str(self.__jobStart) + "-" + self.__jobEnd + ":"
        for curJob in self.__jobDuties:
            retString += curJob + ", "
        print(retString)
        return retString