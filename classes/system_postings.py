import uuid
import datetime as dt
from classes import employee
from classes import sqlmanager
from abc import abstractmethod, ABC


class PaymentSchedule(ABC):
    @abstractmethod
    def do_payment(self):
        pass

    @staticmethod
    def pay_msg(Func, date, Payment):
        print("-----------------------")
        print("Payment Done")
        print("Employee: ", getattr(Func, "name"))
        print("Value: ", Payment)
        print("Paymethod: ", getattr(Func, "payMethod"))
        print("Date: ", date)
        print("-----------------------")


class WeeklySchedule(PaymentSchedule):
    def do_payment(self, days=0, value=0):
        emp_mgr = sqlmanager.EmployeeManager()

        date = dt.date.today()

        z = 0
        while z <= days:
            name_list = emp_mgr.search('hourly', 1)

            if name_list:
                lgt = len(name_list)

                if not value:
                    self.regular_payment(name_list, lgt, emp_mgr, date)
                else:
                    self.non_regular_payment(name_list, lgt, emp_mgr, date)
            else:
                return

            z += 1
            date += dt.timedelta(1)

    def regular_payment(self, name_list, lgt, DbManager, date):
        c = 0

        while c < lgt:
            if name_list[c]:
                Func = employee.Hourly()
                Func.construct_by_select(DbManager.search(name_list[c], 0))

                if date == getattr(Func, "nextPayment") and getattr(Func, "payType").lower() == 'hourly wage':
                    self.pay_make(Func, DbManager, date)
            c += 1

    def non_regular_payment(self, name_list, lgt, DbManager, date):
        c = 0

        while c < lgt:
            if name_list[c]:
                Func = employee.Hourly()
                Func.construct_by_select(DbManager.search(name_list[c], 0))

                if getattr(Func, "payType").lower() == 'monday' and date.weekday() == 0:
                    self.pay_make(Func, DbManager, date)
                elif getattr(Func, "payType").lower() == 'tuesday' and date.weekday() == 1:
                    self.pay_make(Func, DbManager, date)
                elif getattr(Func, "payType").lower() == 'wednessday' and date.weekday() == 2:
                    self.pay_make(Func, DbManager, date)
                elif getattr(Func, "payType").lower() == 'thursday' and date.weekday() == 3:
                    self.pay_make(Func, DbManager, date)
                elif getattr(Func, "payType").lower() == 'friday' and date.weekday() == 4:
                    self.pay_make(Func, DbManager, date)

            c += 1

    def pay_make(self, Func, DbManager, date):
        extra = Func.get_extra_work_hours()
        normal = getattr(Func, "workedHours") - extra

        if extra == 0:
            extra = 1
        if normal == 0:
            normal = 1

        payment = (normal * int(getattr(Func, "wage"))) + ((extra * int(getattr(Func, "wage"))) * 1.5) \
                  - (getattr(Func, "serviceCharge") + getattr(Func, "syndicateCharge"))

        DbManager.update(getattr(Func, "name"), date + dt.timedelta(7), "nextPayment")
        DbManager.update(getattr(Func, "name"), 0, "workedHours")
        DbManager.update(getattr(Func, "name"), 0, "serviceCharge")

        self.pay_msg(Func, date, payment)


class TwoWeeklySchedule(PaymentSchedule):
    def do_payment(self, days=0):
        emp_mgr = sqlmanager.EmployeeManager()

        date = dt.date.today()

        z = 0
        while z <= days:
            name_list = emp_mgr.search('commissioned', 1)

            if name_list:
                lgt = len(name_list)

                self.pay_make(name_list, lgt, emp_mgr, date)
            else:
                return

            z += 1
            date += dt.timedelta(1)

    def pay_make(self, name_list, lgt, DbManager, date):
        c = 0

        while c < lgt:
            if name_list[c]:
                cmsd = employee.Commissioned()

                cmsd.construct_by_select(DbManager.search(name_list[c]))

                if date == getattr(cmsd, "nextPayment") and getattr(cmsd, "payType").lower() == 'commission':
                    payment = cmsd.get_payment(getattr(cmsd, "name")) - \
                              (getattr(cmsd, "syndicateCharge") + getattr(cmsd, "serviceCharge"))

                    DbManager.update(getattr(cmsd, "name"), date + dt.timedelta(15), "nextPayment")
                    DbManager.update(getattr(cmsd, "name"), 0, "sellCount")
                    DbManager.update(getattr(cmsd, "name"), 0, "serviceCharge")

                    self.pay_msg(cmsd, date, payment)
            c += 1


class MonthlySchedule(PaymentSchedule):
    def do_payment(self, days=0):
        emp_mgr = sqlmanager.EmployeeManager()

        date = dt.date.today()

        z = 0
        while z <= days:
            name_list = emp_mgr.search('salaried', 1)

            if name_list:
                lgt = len(name_list)

                self.pay_make(name_list, lgt, emp_mgr, date)

            else:
                return
            z += 1
            date += dt.timedelta(1)

    def pay_make(self, name_list, lgt, DbManager, date):
        c = 0

        while c < lgt:
            if name_list[c]:
                sal = employee.Hourly()

                sal.construct_by_select(DbManager.search(name_list[c]))

                if date == getattr(sal, "nextPayment") and getattr(sal, "payType").lower() == 'monthly salary':
                    payment = getattr(sal, "wage") - (getattr(sal, "syndicateCharge") + getattr(sal, "serviceCharge"))

                    DbManager.update(getattr(sal, "name"),  date + dt.timedelta(30), "nextPayment")
                    DbManager.update(getattr(sal, "name"), 0, "serviceCharge")

                    self.pay_msg(sal, date, payment)
            c += 1


class PointCard(employee.Hourly):
    def get_point_card(self):
        if getattr(self, "pointCardId") is None:
            setattr(self, "pointCardId", str(uuid.uuid4()))
        return

    def post_point_card(self, arrival, departure):
        setattr(self, "workedHours", getattr(self, "workedHours") + (departure - arrival))
        return getattr(self, "workedHours")


class SalePost(employee.Commissioned):
    # Method that generate a uuid for the sale transaction and get the
    # details of the sale
    def get_sale(self, buyerName, value):
        setattr(self, "buyerName", buyerName)
        setattr(self, "salePrice", value)
        setattr(self, "saleDate", dt.date.today().strftime('%Y-%m-%d'))
        self.update_sell_count()
        setattr(self, "saleId", str(uuid.uuid4()))

    # Method that returns the informations stored of sale
    def post_new_sale(self):
        return list(
            [getattr(self, "saleId"), getattr(self, "name"), getattr(self, "buyerName"),
             getattr(self, "saleDate"), getattr(self, "salePrice")]
        )
