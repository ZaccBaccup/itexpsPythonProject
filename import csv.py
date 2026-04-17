
#CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink

from datetime import date


class JobApplication:

    def __init__(self,companyName,jobTitle,appDay,appMonth,appYear,jobLink,isFollowedUp):
        self.__companyName = companyName
        self.__jobTitle = jobTitle
        self.__applyDate = date(appYear,appMonth,appDay)
        self.__jobLink = jobLink
        self.__isFollowedUp = isFollowedUp
        # self.__AppDay = AppDay
        # self.__AppMonth = AppMonth
        # self.__AppYear = AppYear

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
        return [self.__companyName, self.__jobTitle, self.__applyDate.day, self.__applyDate.month, self.__applyDate.year, self.__jobLink, self.__isFollowedUp]