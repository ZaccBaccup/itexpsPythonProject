class Resume:

    def __init__(self, paramList):
        self.__name = ""
        self.__jobTitle = ""
        self.__location = ""
        self.__highestEdu = []
        self.__prevJobs = []
        for curRow in paramList:
            pass



class PreviousJob:
    def __init__(self,initList):
        try:
            self.__jobDuties = [] 
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
            print("Adding ", i,"to object",self)
        
    def ReturnAllJobData(self):
        retString = ""
        retString+=self.__jobRole + ", " + self.__employer + ", " +str(self.__jobStart) + "-" + self.__jobEnd + ":"
        for curJob in self.__jobDuties:
            retString += curJob + ", "
        print(retString)
        return retString