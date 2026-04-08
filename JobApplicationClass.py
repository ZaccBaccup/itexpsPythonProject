
#CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink

from datetime import date


class JobApplication:

    def __init__(self,CompanyName,JobTitle,AppDay,AppMonth,AppYear,JobLink):
        self.__CompanyName = CompanyName
        self.__JobTitle = JobTitle
        self.__ApplyDate = date(AppYear,AppMonth,AppDay)
        self.__JobLink = JobLink
        # self.__AppDay = AppDay
        # self.__AppMonth = AppMonth
        # self.__AppYear = AppYear

    def GetApplyDate(self):
        return self.__ApplyDate
    def GetCompanyName(self):
        return self.__CompanyName
    
    def GetJobTitle(self):
        return self.__JobTitle

    def GetJobLink(self):
        return self.__JobLink