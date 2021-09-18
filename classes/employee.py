import abc

from classes import sqlmanager
from abc import abstractmethod


class Employee:
    def __init__(self, name, address, payMethod, syndicate,
                 syndicateCharge, serviceCharge):
        self.name = name
        self.address = address
        self.payMethod = payMethod
        self.isInSyndicate = syndicate
        self.syndicateCharge = syndicateCharge
        self.serviceCharge = serviceCharge

    @abstractmethod
    def construct_by_select(self, select_result):
        pass

    def common_attr_by_select(self, select_result):
        setattr(self, "name", getattr(select_result, "name"))
        setattr(self, "address", getattr(select_result, "address"))
        setattr(self, "payType", getattr(select_result, "payType"))
        setattr(self, "payMethod", getattr(select_result, "payMethod"))
        setattr(self, "isInSyndicate", getattr(select_result, "isInSyndicate"))
        setattr(self, "syndicateCharge", getattr(select_result, "syndicateCharge"))
        setattr(self, "serviceCharge", getattr(select_result, "serviceCharge"))
        setattr(self, "nextPayment", getattr(select_result, "nextPayment"))
        setattr(self, "wage", float(getattr(select_result, "wage")))


class Hourly(Employee):
    def __init__(self, name=None, address=None, payMethod=None, syndicate=False,
                 syndicateCharge=None, serviceCharge=None, nextPayment=None, wage=None):
        super().__init__(name, address, payMethod, syndicate, syndicateCharge, serviceCharge)
        self.payType = None
        self.nextPayment = nextPayment
        self.wage = wage
        self.pointCardId = None
        self.workedHours = None

    def get_extra_work_hours(self):
        extra = 56 - (getattr(self, "workedHours") / 7)
        if extra > 0:
            return 0
        else:
            return extra * (-1)

    # Method that constructs our class from the result of SELECT query in database
    def construct_by_select(self, select_result):
        self.common_attr_by_select(select_result)
        setattr(self, "pointCardId", getattr(select_result, "pointCardId"))
        setattr(self, "workedHours", getattr(select_result, "workedHours"))


class Commissioned(Employee):
    def __init__(self, name=None, address=None, payMethod=None, syndicate=False, syndicateCharge=None,
                 serviceCharge=None, nextPayment=None, wage=None):
        super().__init__(name, address, payMethod, syndicate, syndicateCharge, serviceCharge)
        self.payType = None
        self.wage = wage
        self.nextPayment = nextPayment
        self.saleDate = None
        self.salePrice = None
        self.saleId = None
        self.buyerName = None
        self.sellCount = 0
        self.commissionPercent = None

    # Method that updates our employee's sell counter
    def update_sell_count(self):
        setattr(self, "sellCount", getattr(self, "sellCount") + 1)

    # Method that returns our employee's sell counter
    def get_sell_count(self):
        return getattr(self, "sellCount")

    # Method that takes the total sales amount of the commissioned to calculate
    # the commission rate and calculate the employee's total payment
    def get_payment(self, name):
        TempMGR = sqlmanager.SalesManager()

        totalSells = TempMGR.search(name)

        if totalSells:
            return getattr(self, "wage") + (float(getattr(self, "commissionPercent")) * totalSells)

        return getattr(self, "wage")

    # Method that constructs our class from the result of SELECT query in database
    def construct_by_select(self, select_result):
        self.common_attr_by_select(select_result)
        setattr(self, "sellCount", getattr(select_result, "sellCount"))
        setattr(self, "saleId", None)
        setattr(self, "saleDate", None)
        setattr(self, "salePrice", None)
        setattr(self, "buyerName", None)
        setattr(self, "commissionPercent", getattr(select_result, "commissionPercent"))
