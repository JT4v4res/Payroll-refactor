from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Date, Float
import datetime as dt
from abc import abstractmethod, ABC

# MySQL connector defined
engine = create_engine("mysql+pymysql://user:password@localhost:port/database", echo=False)

# Define and create table
Base = declarative_base()

# Session for SQLALCHEMY's ORM
Session = sessionmaker(bind=engine)
session = Session()


class PersoSchedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    dayCode = Column(Integer)
    scheDs = Column(String(15))

    def __init__(self, id, dayCode, scheDs):
        self.id = id
        self.dayCode = dayCode
        self.scheDs = scheDs


class Syndicate(Base):
    __tablename__ = 'syndicate'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(55))
    address = Column(String(90))
    syndicateCharge = Column(Integer)
    serviceCharge = Column(Integer)

    def __init__(self, id, name, address, syndicateCharge, serviceCharge):
        self.id = id
        self.name = name
        self.address = address
        self.syndicateCharge = syndicateCharge
        self.serviceCharge = serviceCharge


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    saleId = Column(String(80))
    sellerName = Column(String(55))
    buyerName = Column(String(55))
    saleDate = Column(Date)
    salePrice = Column(Float)
    wasCommissioned = Column(Boolean)

    def __init__(self, saleId, sellerName, buyerName, saleDate, salePrice, wasCommissioned):
        self.saleId = saleId
        self.sellerName = sellerName
        self.buyerName = buyerName
        self.saleDate = saleDate
        self.salePrice = salePrice
        self.wasCommissioned = wasCommissioned


# This class provides our mapping and planning for implementing and manipulating
# data and other functionality relating to our payroll employees.
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = Column(String(55))
    address = Column(String(90))
    jType = Column(String(25))
    payType = Column(String(25))
    payMethod = Column(Integer)
    isInSyndicate = Column(Boolean)
    syndicateCharge = Column(Integer)
    serviceCharge = Column(Integer)
    nextPayment = Column(Date)
    wage = Column(Float)
    pointCardId = Column(String(80))
    workedHours = Column(Integer)
    sellCount = Column(Integer)
    commissionPercent = Column(Float)

    def __init__(self, id, name, address, jType, payType, payMethod, isInSyndicate, syndicateCharge,
                 serviceCharge, nextPayment, wage, pointCardId, workedHours, sellCount, commissionPercent):
        self.id = id
        self.name = name
        self.address = address
        self.jType = jType
        self.payType = payType
        self.payMethod = payMethod
        self.isInSyndicate = isInSyndicate
        self.syndicateCharge = syndicateCharge
        self.serviceCharge = serviceCharge
        self.nextPayment = nextPayment
        self.wage = wage
        self.pointCardId = pointCardId
        self.workedHours = workedHours
        self.sellCount = sellCount
        self.commissionPercent = commissionPercent


# This class provides the management and
# manipulation of all transactions made with the database.
class SQLManager(ABC):
    # Method responsible for performing the insertion operation in a table
    # in our database, using the parameters specified in the class attributes and received from method call.
    def insert(self, value):
        try:
            session.add(value)
            session.commit()

            self.success_msg("Insert")
        except exc.SQLAlchemyError as err:
            self.fail_msg("insert", err)
        finally:
            self.close_msg()

    def delete(self, value):
        try:
            To_rmv = self.search(value)

            if To_rmv:
                session.delete(To_rmv)
                session.commit()

            self.success_msg("Delete")
        except exc.SQLAlchemyError as err:
            self.fail_msg("delete", err)
        finally:
            self.close_msg()

    @abstractmethod
    def search(self, value):
        pass

    def update(self, value, value2, attr):
        try:
            Func = self.search(value)

            if Func:
                setattr(Func, attr, value2)
                session.commit()

            self.success_msg("Update")
        except exc.SQLAlchemyError as err:
            self.fail_msg("update", err)
        finally:
            self.close_msg()

    @staticmethod
    def success_msg(operation):
        print("----------------------------")
        print(f"{operation} completed successfully")

    @staticmethod
    def fail_msg(operation, err):
        print("----------------------------")
        print("Failed to {} in table: {}".format(operation, err))

    @staticmethod
    def close_msg():
        print("----------------------------")
        print("Closed connection")
        print("----------------------------")


class EmployeeManager(SQLManager):
    def search(self, value, opt=0):
        slct = None

        try:
            if opt == 0:
                slct = session.query(Employee).filter(Employee.name == value).first()
            else:
                query = session.query(Employee).filter(Employee.jType == value).all()
                slct = []

                for c in query:
                    slct.append(c.name)

            self.success_msg("Search")
        except exc.SQLAlchemyError as err:
            self.fail_msg("search", err)
        finally:
            self.close_msg()
            return slct

    def update_type(self, e_name, value=None, value2=None, value3=None, value4=None):
        self.update(e_name, value, "commissionPercent")
        self.update(e_name, value2, "sellCount")
        self.update(e_name, value3, "workedHours")
        self.update(e_name, value4, "pointCardId")


class SalesManager(SQLManager):
    def search(self, value):
        slct = None
        try:
            query = session.query(Sales).filter(Sales.sellerName == value).all()
            slct = 0
            for i in query:
                slct += i.salePrice
                self.update(getattr(i, "name"), 1, "wasCommissioned")

            self.success_msg("Search")
        except exc.SQLAlchemyError as err:
            self.fail_msg("search", err)
        finally:
            self.close_msg()
            return slct


class SyndicateManager(SQLManager):
    def search(self, value):
        slct = None
        try:
            slct = session.query(Syndicate).filter(Syndicate.name == value).first()

            self.success_msg("Search")
        except exc.SQLAlchemyError as err:
            self.fail_msg("search", err)
        finally:
            self.close_msg()
            return slct


class SchManager(SQLManager):
    def search(self, value):
        slct = None

        try:
            slct = session.query(PersoSchedule).filter(PersoSchedule.scheDs == value).first()
        except exc.SQLAlchemyError as err:
            self.fail_msg("search", err)
        finally:
            self.close_msg()
            return slct
