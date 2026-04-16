
#CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink

from datetime import date


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