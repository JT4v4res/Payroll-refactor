# Payroll Refactoring

This repository presents a refactored version
of the project present in [Payroll-System](https://github.com/JT4v4res/Payroll-System),
a payroll system made for the
purpose of evaluating the subject of Programming 2/Software Project.

The refactoring was performed as a way to correct and eliminate
the code smells identified in the original system.

![](https://media.giphy.com/media/2lAquPl05GqQ4R7YsZ/giphy.gif?cid=790b76118ed92bbb40d400afd30eea1d5f684188c4a5f9e8&rid=giphy.gif&ct=g)

Several code smells were identified and fixed in the original code, we will now talk about the identified smells and how they were fixed.

## Code Smells Detected

|code smell detected|Source|Standard applied|
|---|---|---|
|Large Class|- Very large **SQLManager** class, with about 200 lines of code in this class alone, dealing with many unnecessary fields and actions.<br><br> - **PaymentSchedule** class was another very large class, with over 150 lines and handling a lot of unnecessary actions too.|- Here we applied **Extract Class** and **Extract Subclass**, together with **Factory Method**, where from class **SQLManager** we extract 4 subclasses, each one to deal with a specific table, and from **PaymentSchedule** we extract 3 classes, each one for the purpose of handling the payment of one type of employee.|
|Long Method|- **SQLManager** contained two gigantic methods that had to deal with a lot of parameters and had a lot of IF's and Else's.<br><br> - The class **PaymentSchedule** also featured giant methods, the main **Long Method** being **WeeklyPayment**.|- **Extract Method** applied, during **Extract Class** application, to remove the **search** methods and the 3 payment methods from the **SQLManager** and **PaymentSchedule** classes, with the use of inheritance patterns and polymorphism in both classes and new methods to solve the smell.|
|Middle Man|- **getPointCard** method only called another method that it could execute.<br><br> - **getSaleId** method only executed a line of code used only once and that could be directly assigned in the method in which it was called.|- **Extract Method** used to remove the methods and apply the **Inline Method** to insert the single lines of code in the methods that called them.|
|Speculative Generality|- The **Employee** class and its derivatives had unused methods, these being **getEmployeeName** and **getAttributesTuple** that were not used for anything.|- Application of **Remove Method** to remove both methods, since both methods were not used anywhere in the code.|
|Duplicate Code|- In the implementation of employees, the method of building employees from the database query had repeated code in attributes common to all employees.<br><br> - **SQLManager** had many lines of code repeated in success, failure, and database connection/transaction termination messages, plus lines of code that could be replaced by a line to make the method cleaner and more dynamic.<br><br> - **PaymentSchedule** featured many repeating lines of code, in addition to IF's and Else's with many repeating lines and little dynamism.|- **Extract Method** used to transform the success, error and connection end messages into methods to avoid code repetition, in addition to applying **Consolidate Conditional Expression** to simplify conditionals into simple and dynamic expressions, and creating a method to avoid repeating the lines of instantiation of attributes common to all employees.|


## Simple Code Smells Resolved

The following section presents the smells solved with simple patterns, being them
**Speculative Generality** and **Duplicate Code**, identified in the **SQLManager**,
**PaymentSchedule** and in the employee classes.

### PaymentSchedule

- The **PayWeekly** method presents itself as a **Long Method** and had many
repeated lines of code, to solve the repeated 
lines of code we used the **Extract Method** pattern.
<br><br>
- In addition, there were also many conditionals with a lot of repeated code, 
they were simplified with the **Extract Method**,
as we created a new method to execute the duplicate code block.

[Original Duplicate Code and Repeated Conditional](https://github.com/JT4v4res/Payroll-System/blob/main/classes/system_postings.py#L52-L169) <br>
[Refactor Done in Duplicate Code](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/system_postings.py#L8-L21) <br>
[Refactor Done in Repeated Conditional](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/system_postings.py#L62-L78)

Below are the original and refactored code:

Original code snippet:
```python
if not value:
    while c < lgt:
        if name_list[c]:
            Func = employee.Hourly()
            Func.constructHourlyFSelect(DbManager.searchInTable(name_list[c], 0))

            if date == Func.nextPayment and Func.payType.lower() == 'hourly wage':
                Extra = Func.getExtraWorkHours()
                Normal = Func.workedHours - Extra

                if Extra == 0:
                    Extra = 1
                if Normal == 0:
                    Normal = 1

                Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5)\
                          - (Func.serviceCharge + Func.syndicateCharge)

                DbManager.updateTable(name_list[c], up_op=6, date=date)

                print("-----------------------")
                print("Payment Done")
                print("Employee: ", Func.getEmployeeName())
                print("Value: ", Payment)
                print("Paymethod: ", Func.payMethod)
                print("Date: ", date)
                print("-----------------------")
        c += 1
else:
    while c < lgt:
        if name_list[c]:
            Func = employee.Hourly()
            Func.constructHourlyFSelect(DbManager.searchInTable(name_list[c], 0))

            if Func.payType.lower() == 'monday':
                if date.weekday() == 0:
                    Extra = Func.getExtraWorkHours()
                    Normal = Func.workedHours - Extra

                    if Extra == 0:
                        Extra = 1
                    if Normal == 0:
                        Normal = 1

                    Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5) \
                              - (Func.serviceCharge + Func.syndicateCharge)

                    DbManager.updateTable(name_list[c], up_op=6, date=date)

                    print("-----------------------")
                    print("Payment Done")
                    print("Employee: ", Func.getEmployeeName())
                    print("Value: ", Payment)
                    print("Paymethod: ", Func.payMethod)
                    print("Date: ", date)
                    print("-----------------------")
```

Small excerpt demonstrating the repetition of codes and a portion of the repeated conditionals

```python
@staticmethod
def pay_msg(Func, date, Payment):
    print("-----------------------")
    print("Payment Done")
    print("Employee: ", getattr(Func, "name"))
    print("Value: ", Payment)
    print("Paymethod: ", getattr(Func, "payMethod"))
    print("Date: ", date)
    print("-----------------------")
```

Method to replace repeated portions of code.

```python
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
```

The refactored portion of conditionals simplified with the **Extract Method**.

### SQLManager

- This class presents code snippets repeated several times unnecessarily, 
using **Extract Method** this has been fixed. <br><br>
- The **Update** method had several IF's and Else's that could be simplified into an expression
that would make the method more dynamic, in addition to eliminating unnecessary conditionals.

[Original Duplicate Code](https://github.com/JT4v4res/Payroll-System/blob/main/classes/sqlmanager.py#L116-L154) <br>
[Original Repeated Conditional](https://github.com/JT4v4res/Payroll-System/blob/main/classes/sqlmanager.py#L158-L253) <br>
[Refactor Duplicate Code](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/sqlmanager.py#L157-L171) <br>
[Refactor Repeated Conditional](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/sqlmanager.py#L139-L155) <br>

Below are the original implementations and the refactored version:

Original code snippet:
```python
# Method responsible for performing the insertion operation in a table
# in our database, using the parameters specified in the class attributes and received from method call.
def insertInTable(self, value):
    try:
        session.add(value)
        session.commit()

        print("----------------------------")
        print("Successfully inserted")
    except exc.SQLAlchemyError as err:
        print("----------------------------")
        print("Failed to insert in table: {}".format(err))
    finally:
        print("----------------------------")
        print("Closed connection")
        print("----------------------------")


# Method responsible for performing the remove operation on a table in our database, using the
# parameters specified in the class attributes and received from the method call
def deleteFromTable(self, value, opt):
    try:
        To_rmv = self.searchInTable(value, 0)
        To_rmv_synd = self.searchInTable(value, 3)
        if opt == 2:
            To_rmv.isInSyndicate = 0
            session.delete(To_rmv_synd)
        else:
            session.delete(To_rmv)
            if To_rmv_synd:
                session.delete(To_rmv_synd)
        session.commit()
        print("----------------------------")
        print("Successfully removed")
    except exc.SQLAlchemyError as err:
        print("----------------------------")
        print("Failed to delete from table: {}".format(err))
    finally:
        print("----------------------------")
        print("Closed connection")
        print("----------------------------")
```

And the original implementation of the update method with conditionals.

```python
# Method that updates an employee's record in our table
# up_op is used to decide whether to change our employee's address or work type
def updateTable(self, value, value2=None, up_op=None, date=None):
    try:
        if up_op == 0:
            hFunc = self.searchInTable(value, 0)
            hFunc.workedHours = value2

            session.commit()
        elif up_op == 1:
            sFunc = self.searchInTable(value, 0)
            sFunc.sellCount = value2

            session.commit()
        elif up_op == 2:
            chrgFunc = self.searchInTable(value, 0)
            chrgFunc.serviceCharge = value2

            session.commit()
        elif up_op == 3:
            addrFunc = self.searchInTable(value, 0)
            addrFunc.address = value2

            addrSynd = self.searchInTable(value, 3)
            if addrSynd:
                addrSynd.address = value2

            session.commit()
        elif up_op == 4:
            typFunc = self.searchInTable(value, 0)

            typFunc.jType = value2
            typFunc.payType = jTypes[value2]

            session.commit()
```

Now the refactored versions of those code snippets.

```python
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
```

Code snippet of simplified conditionals.

```python
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
```

### Employee Mapping Classes

- **Duplicate Code** in a method common to the 3 classes. <br><br>
- **Speculative Generality** detected in **getplayerName** and **getEmployeeTypeAttributes** methods.

[Original Duplicate Code](https://github.com/JT4v4res/Payroll-System/blob/main/classes/employee.py#L6-L170) <br>
[Original Speculative Generality](https://github.com/JT4v4res/Payroll-System/blob/main/classes/employee.py#L22-L32) <br>
[Refator Duplicate Code and Speculative Generality](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/employee.py#L7-L30) <br>

Original code snippet:
```python
# Method that returns our employee's name
def getEmployeeName(self):
    return self.name

# Method that returns our character's attributes as a tuple so we can access
# them without having to directly access the attributes in the class
def getSalariedAttributes(self):
    return tuple(
        [self.name, self.address, self.jType, self.payMethod, self.isInSyndicate,
         self.syndicateCharge, self.serviceCharge, self.nextPayment, self.wage, None, None, None]
    )

# Method that constructs our class from the result of SELECT query in database
def constructSalFSelect(self, SelectResult):
    self.id = SelectResult.id
    self.name = SelectResult.name
    self.address = SelectResult.address
    self.jType = SelectResult.jType
    self.payType = SelectResult.payType
    self.payMethod = SelectResult.payMethod
    self.isInSyndicate = SelectResult.isInSyndicate
    self.syndicateCharge = SelectResult.syndicateCharge
    self.serviceCharge = SelectResult.serviceCharge
    self.nextPayment = SelectResult.nextPayment
    self.wage = int(SelectResult.wage)
```

Above, a portion of the repeated code and the two **Speculative Generality** methods.
```python
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

    # Method that constructs our class from the result of SELECT query in database
    def construct_by_select(self, select_result):
        self.common_attr_by_select(select_result)
        setattr(self, "pointCardId", getattr(select_result, "pointCardId"))
        setattr(self, "workedHours", getattr(select_result, "workedHours"))
```

Above the refactored portion with **Extract Method** and **Remove Method**, the abstract method
has been inserted together for a demonstration of the implementation of the abstract method.

## Complex Code Smells Resolved

This section presents fixes for complex smells, solved using polymorphism and inheritance concepts,
identified in the **SQLManager**, **PaymentSchedule** and in the employee classes.

### SQLManager

**Large Class** with **Long Method**, methods performing various tasks and unnecessary comparisons
that could be solved by applying the
concepts of polymorphism and inheritance, in addition to applying **Extract Class** and **Extract Method**.

[Original Large Class with Large Method](https://github.com/JT4v4res/Payroll-System/blob/main/classes/sqlmanager.py#L109-L290) <br>
[Refactored Base Class](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/sqlmanager.py#L109-L171) <br>
[New Subclasses Made in Refactor](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/sqlmanager.py#L174-L244) <br>

Original code snippet:
```python
# This class provides the management and
# manipulation of all transactions made with the database.
class SQLManager:
    pass

    # Method responsible for performing the insertion operation in a table
    # in our database, using the parameters specified in the class attributes and received from method call.
    def insertInTable(self, value):
        try:
            session.add(value)
            session.commit()

            print("----------------------------")
            print("Successfully inserted")
        except exc.SQLAlchemyError as err:
            print("----------------------------")
            print("Failed to insert in table: {}".format(err))
        finally:
            print("----------------------------")
            print("Closed connection")
            print("----------------------------")


    # Method responsible for performing the remove operation on a table in our database, using the
    # parameters specified in the class attributes and received from the method call
    def deleteFromTable(self, value, opt):
        try:
            To_rmv = self.searchInTable(value, 0)
            To_rmv_synd = self.searchInTable(value, 3)
            if opt == 2:
                To_rmv.isInSyndicate = 0
                session.delete(To_rmv_synd)
            else:
                session.delete(To_rmv)
                if To_rmv_synd:
                    session.delete(To_rmv_synd)
            session.commit()
            print("----------------------------")
            print("Successfully removed")
        except exc.SQLAlchemyError as err:
            print("----------------------------")
            print("Failed to delete from table: {}".format(err))
        finally:
            print("----------------------------")
            print("Closed connection")
            print("----------------------------")

    # Method that updates an employee's record in our table
    # up_op is used to decide whether to change our employee's address or work type
    def updateTable(self, value, value2=None, up_op=None, date=None):
        try:
            if up_op == 0:
                hFunc = self.searchInTable(value, 0)
                hFunc.workedHours = value2

                session.commit()
            elif up_op == 1:
                sFunc = self.searchInTable(value, 0)
                sFunc.sellCount = value2

                session.commit()
            elif up_op == 2:
                chrgFunc = self.searchInTable(value, 0)
                chrgFunc.serviceCharge = value2

                session.commit()
            elif up_op == 3:
                addrFunc = self.searchInTable(value, 0)
                addrFunc.address = value2

                addrSynd = self.searchInTable(value, 3)
                if addrSynd:
                    addrSynd.address = value2

                session.commit()
            elif up_op == 4:
                typFunc = self.searchInTable(value, 0)

                typFunc.jType = value2
                typFunc.payType = jTypes[value2]

                session.commit()
            elif up_op == 5:
                nnameFunc = self.searchInTable(value, 0)
                nnameFunc.name = value2

                nameSynd = self.searchInTable(value, 3)
                if nameSynd:
                    nameSynd.name = value2

                query = session.query(Sales).filter(Sales.sellerName == value).all()

                if query:
                    for i in query:
                        i.name = value2

                session.commit()
            elif up_op == 6:
                Funct = self.searchInTable(value, 0)
                if Funct.jType.lower() == 'hourly':
                    Funct.nextPayment = date + dt.timedelta(7)
                    Funct.workedHours = 0
                    Funct.serviceCharge = 0
                    session.commit()
                elif Funct.jType.lower() == 'commissioned':
                    Funct.nextPayment = date + dt.timedelta(15)
                    Funct.sellCount = 0
                    Funct.serviceCharge = 0
                    session.commit()
                else:
                    Funct.nextPayment = date + dt.timedelta(30)
                    Funct.serviceCharge = 0
                    session.commit()
            elif up_op == 7:
                func = self.searchInTable(value, 0)
                if func:
                    func.syndicateCharge = value2

                syndFunc = self.searchInTable(value, 3)
                if syndFunc:
                    syndFunc.syndicateCharge = value2

                session.commit()
            elif up_op == 8:
                func = self.searchInTable(value, 0)
                func.payType = value2

                session.commit()
            elif up_op == 9:
                query = session.query(Sales).filter(Sales.sellerName == value).all()

                for i in query:
                    i.wasCommissioned = 1

                session.commit()

            print("----------------------------")
            print("Table updated successfully")
        except exc.SQLAlchemyError as err:
            print("----------------------------")
            print("Failed to update table: {}".format(err))
        finally:
            print("----------------------------")
            print("Closed connection")
            print("----------------------------")


    # Method responsible for performing a name lookup in
    # our tables, the method can be used to acquire information
    # about an employee to update reassemble the respective employee's class
    def searchInTable(self, value, opt):
        slct = None

        try:
            if opt == 0:
                slct = session.query(Employee).filter(Employee.name == value).first()
            elif opt == 1:
                query = session.query(Sales).filter(Sales.sellerName == value).all()
                slct = 0
                for i in query:
                    slct += i.salePrice

            elif opt == 2:
                query = session.query(Employee).filter(Employee.jType == value).all()
                slct = []

                for c in query:
                    slct.append(c.name)

            elif opt == 3:
                slct = session.query(Syndicate).filter(Syndicate.name == value).first()

            print("----------------------------")
            print("Search completed successfully")
        except exc.SQLAlchemyError as err:
            print("----------------------------")
            print("Failed to search in table: {}".format(err))
        finally:
            print("----------------------------")
            print("Closed connection")
            print("----------------------------")
            return slct
```

Refactored class and its subclasses:
```python
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
```

### PaymentSchedule

Another **Large Class** with **Long Method**, from the application 
of **Extract Method** and **Extract Class** the smells were solved/alleviated.

[Original Large Class](https://github.com/JT4v4res/Payroll-System/blob/main/classes/system_postings.py#L7-L258) <br>
[Refactored Base Class](https://github.com/JT4v4res/Payroll-System/blob/main/classes/system_postings.py#L7-L258) <br>
[New Subclasses](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/system_postings.py#L24-L176) <br>

Original code snippet:
```python
class PaymentSchedule:
    def __init__(self):
        pass

    def payWeekly(self, days=0, value=None):
        DbManager = sqlmanager.SQLManager()

        date = dt.date.today()

        z = 0
        while z <= days:
            name_list = DbManager.searchInTable('hourly', 2)

            if name_list:
                lgt = len(name_list)

                c = 0
                if not value:
                    while c < lgt:
                        if name_list[c]:
                            Func = employee.Hourly()
                            Func.constructHourlyFSelect(DbManager.searchInTable(name_list[c], 0))

                            if date == Func.nextPayment and Func.payType.lower() == 'hourly wage':
                                Extra = Func.getExtraWorkHours()
                                Normal = Func.workedHours - Extra

                                if Extra == 0:
                                    Extra = 1
                                if Normal == 0:
                                    Normal = 1

                                Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5)\
                                          - (Func.serviceCharge + Func.syndicateCharge)

                                DbManager.updateTable(name_list[c], up_op=6, date=date)

                                print("-----------------------")
                                print("Payment Done")
                                print("Employee: ", Func.getEmployeeName())
                                print("Value: ", Payment)
                                print("Paymethod: ", Func.payMethod)
                                print("Date: ", date)
                                print("-----------------------")
                        c += 1
                else:
                    while c < lgt:
                        if name_list[c]:
                            Func = employee.Hourly()
                            Func.constructHourlyFSelect(DbManager.searchInTable(name_list[c], 0))

                            if Func.payType.lower() == 'monday':
                                if date.weekday() == 0:
                                    Extra = Func.getExtraWorkHours()
                                    Normal = Func.workedHours - Extra

                                    if Extra == 0:
                                        Extra = 1
                                    if Normal == 0:
                                        Normal = 1

                                    Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5) \
                                              - (Func.serviceCharge + Func.syndicateCharge)

                                    DbManager.updateTable(name_list[c], up_op=6, date=date)

                                    print("-----------------------")
                                    print("Payment Done")
                                    print("Employee: ", Func.getEmployeeName())
                                    print("Value: ", Payment)
                                    print("Paymethod: ", Func.payMethod)
                                    print("Date: ", date)
                                    print("-----------------------")
                            elif Func.payType.lower() == 'tuesday':
                                if date.weekday() == 1:
                                    Extra = Func.getExtraWorkHours()
                                    Normal = Func.workedHours - Extra

                                    if Extra == 0:
                                        Extra = 1
                                    if Normal == 0:
                                        Normal = 1

                                    Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5) \
                                              - (Func.serviceCharge + Func.syndicateCharge)

                                    DbManager.updateTable(name_list[c], up_op=6, date=date)

                                    print("-----------------------")
                                    print("Payment Done")
                                    print("Employee: ", Func.getEmployeeName())
                                    print("Value: ", Payment)
                                    print("Paymethod: ", Func.payMethod)
                                    print("Date: ", date)
                                    print("-----------------------")
                            elif Func.payType.lower() == 'wednessday':
                                if date.weekday() == 2:
                                    Extra = Func.getExtraWorkHours()
                                    Normal = Func.workedHours - Extra

                                    if Extra == 0:
                                        Extra = 1
                                    if Normal == 0:
                                        Normal = 1

                                    Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5) \
                                              - (Func.serviceCharge + Func.syndicateCharge)

                                    DbManager.updateTable(name_list[c], up_op=6, date=date)

                                    print("-----------------------")
                                    print("Payment Done")
                                    print("Employee: ", Func.getEmployeeName())
                                    print("Value: ", Payment)
                                    print("Paymethod: ", Func.payMethod)
                                    print("Date: ", date)
                                    print("-----------------------")
                            elif Func.payType.lower() == 'thursday':
                                if date.weekday() == 3:
                                    Extra = Func.getExtraWorkHours()
                                    Normal = Func.workedHours - Extra

                                    if Extra == 0:
                                        Extra = 1
                                    if Normal == 0:
                                        Normal = 1

                                    Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5) \
                                              - (Func.serviceCharge + Func.syndicateCharge)

                                    DbManager.updateTable(name_list[c], up_op=6, date=date)

                                    print("-----------------------")
                                    print("Payment Done")
                                    print("Employee: ", Func.getEmployeeName())
                                    print("Value: ", Payment)
                                    print("Paymethod: ", Func.payMethod)
                                    print("Date: ", date)
                                    print("-----------------------")
                            elif Func.payType.lower() == 'friday':
                                if date.weekday() == 4:
                                    Extra = Func.getExtraWorkHours()
                                    Normal = Func.workedHours - Extra

                                    if Extra == 0:
                                        Extra = 1
                                    if Normal == 0:
                                        Normal = 1

                                    Payment = (Normal * Func.wage) + ((Extra * Func.wage) * 1.5) \
                                              - (Func.serviceCharge + Func.syndicateCharge)

                                    DbManager.updateTable(name_list[c], up_op=6, date=date)

                                    print("-----------------------")
                                    print("Payment Done")
                                    print("Employee: ", Func.getEmployeeName())
                                    print("Value: ", Payment)
                                    print("Paymethod: ", Func.payMethod)
                                    print("Date: ", date)
                                    print("-----------------------")

                        c += 1
            else:
                return
            z += 1
            date += dt.timedelta(1)

    def pay2Weekly(self, days=0, value=None):
        DbManager = sqlmanager.SQLManager()

        date = dt.date.today()

        z = 0
        while z <= days:
            name_list = DbManager.searchInTable('commissioned', 2)

            if name_list:
                lgt = len(name_list)

                c = 0
                if not value:
                    while c < lgt:
                        if name_list[c]:
                            cmsd = employee.Comissioned()

                            cmsd.constructCommsFSelect(DbManager.searchInTable(name_list[c], 0))

                            if date == cmsd.nextPayment and cmsd.payType.lower() == 'commission':
                                Payment = cmsd.getPayment(cmsd.getEmployeeName()) - \
                                          (cmsd.syndicateCharge + cmsd.serviceCharge)

                                DbManager.updateTable(name_list[c], up_op=6, date=date)

                                print("-----------------------")
                                print("Payment Done")
                                print("Employee: ", cmsd.getEmployeeName())
                                print("Value: ", Payment)
                                print("Paymethod: ", cmsd.payMethod)
                                print("Date: ", date)
                                print("-----------------------")
                        c += 1
            else:
                return
            z += 1
            date += dt.timedelta(1)

    def payMonthly(self, days=0, value=None):
        DbManager = sqlmanager.SQLManager()

        date = dt.date.today()

        z = 0
        while z <= days:
            name_list = DbManager.searchInTable('salaried', 2)

            if name_list:
                lgt = len(name_list)

                c = 0
                if not value:
                    while c < lgt:
                        if name_list[c]:
                            sal = employee.Salaried()

                            sal.constructSalFSelect(DbManager.searchInTable(name_list[c], 0))

                            if date == sal.nextPayment and sal.payType.lower() == 'monthly salary':
                                Payment = sal.wage - sal.syndicateCharge + sal.serviceCharge

                                DbManager.updateTable(name_list[c], up_op=6, date=date)

                                print("-----------------------")
                                print("Payment Done")
                                print("Employee: ", sal.getEmployeeName())
                                print("Value: ", Payment)
                                print("Paymethod: ", sal.payMethod)
                                print("Date: ", date)
                                print("-----------------------")
                        c += 1
            else:
                return
            z += 1
            date += dt.timedelta(1)

    def PersoPayment(self, days=0):
        z = 0
        while z <= days:
            self.payWeekly(days, 1)
            self.pay2Weekly(days, 1)
            self.payMonthly(days, 1)
            z += 1
```

Refactored class and its subclasses:
```python
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
```

### Classes of Employees

The employee classes were implemented separately, having **Duplicate Code** and configuring several **Large Class**.

The **Salaried** class was removed as it also had **Speculative Generality**, it didn't have any additional attributes different 
from the other classes, so it can be replaced by one of the two employee classes **Commissioned** 
or **Hourly**, which can fulfill the role of this type, since it has no differential attributes.

[Original Employees Classes](https://github.com/JT4v4res/Payroll-System/blob/main/classes/employee.py#L6-L170) <br>
[Refactored Base Class](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/employee.py#L7-L30) <br>
[New Subclasses](https://github.com/JT4v4res/Payroll-refactor/blob/main/classes/employee.py#L33-L99) <br>

Original code snippet:
```python
class Hourly:
    def __init__(self, name=None, address=None, payMethod=None,job_Type='hourly', syndicate=False):
        self.id = None
        self.name = name
        self.address = address
        self.jType = job_Type
        self.payType = jTypes[job_Type]
        self.payMethod = payMethod
        self.isInSyndicate = syndicate
        self.syndicateCharge = None
        self.serviceCharge = None
        self.nextPayment = None
        self.wage = None
        self.pointCardId = None
        self.workedHours = None

    # Method that returns our employee's name
    def getEmployeeName(self):
        return self.name

    # Method that returns our character's attributes as a tuple so we can access
    # them without having to directly access the attributes in the class
    def getHourlyAttributes(self):
        return tuple(
            [self.name, self.address, self.jType, self.payType, self.payMethod, self.isInSyndicate, self.syndicateCharge,
             self.serviceCharge, self.nextPayment, str(self.wage), self.pointCardId, self.workedHours, None]
        )

    def getExtraWorkHours(self):
        extra = 56 - (self.workedHours / 7)
        if extra > 0:
            return 0
        else:
            return extra * (-1)

    # Method that constructs our class from the result of SELECT query in database
    def constructHourlyFSelect(self, SelectResult):
        self.id = SelectResult.id
        self.name = SelectResult.name
        self.address = SelectResult.address
        self.jType = SelectResult.jType
        self.payType = SelectResult.payType
        self.payMethod = SelectResult.payMethod
        self.isInSyndicate = SelectResult.isInSyndicate
        self.syndicateCharge = SelectResult.syndicateCharge
        self.serviceCharge = SelectResult.serviceCharge
        self.nextPayment = SelectResult.nextPayment
        self.wage = int(SelectResult.wage)
        self.pointCardId = SelectResult.pointCardId
        self.workedHours = SelectResult.workedHours


class Salaried:
    def __init__(self, name=None, address=None, payMethod=None, job_Type='salaried', syndicate=False):
        self.id = None
        self.name = name
        self.address = address
        self.jType = job_Type
        self.payType = jTypes[job_Type]
        self.payMethod = payMethod
        self.isInSyndicate = syndicate
        self.syndicateCharge = None
        self.serviceCharge = None
        self.nextPayment = None
        self.wage = None

    # Method that returns our employee's name
    def getEmployeeName(self):
        return self.name

    # Method that returns our character's attributes as a tuple so we can access
    # them without having to directly access the attributes in the class
    def getSalariedAttributes(self):
        return tuple(
            [self.name, self.address, self.jType, self.payMethod, self.isInSyndicate,
             self.syndicateCharge, self.serviceCharge, self.nextPayment, self.wage, None, None, None]
        )

    # Method that constructs our class from the result of SELECT query in database
    def constructSalFSelect(self, SelectResult):
        self.id = SelectResult.id
        self.name = SelectResult.name
        self.address = SelectResult.address
        self.jType = SelectResult.jType
        self.payType = SelectResult.payType
        self.payMethod = SelectResult.payMethod
        self.isInSyndicate = SelectResult.isInSyndicate
        self.syndicateCharge = SelectResult.syndicateCharge
        self.serviceCharge = SelectResult.serviceCharge
        self.nextPayment = SelectResult.nextPayment
        self.wage = int(SelectResult.wage)


class Comissioned:
    def __init__(self, name=None, address=None, payMethod=None, job_Type='commissioned', syndicate=False):
        self.id = None
        self.name = name
        self.address = address
        self.jType = job_Type
        self.payType = jTypes[job_Type]
        self.payMethod = payMethod
        self.isInSyndicate = syndicate
        self.syndicateCharge = None
        self.serviceCharge = None
        self.nextPayment = None
        self.wage = None
        self.saleDate = None
        self.salePrice = None
        self.saleId = None
        self.buyerName = None
        self.sellCount = 0
        self.comissionPercent = None

    # Method that returns our employee's name
    def getEmployeeName(self):
        return self.name

    # Method that updates our employee's sell counter
    def updateSellCount(self):
        self.sellCount += 1

    # Method that returns our employee's sell counter
    def getSellCount(self):
        return self.sellCount

    # Method that takes the total sales amount of the commissionee to calculate
    # the commission rate and calculate the employee's total payment
    def getPayment(self, name):
        TempMGR = sqlmanager.SQLManager()

        totalSells = TempMGR.searchInTable(name, 1)

        if totalSells:
            return self.wage + (float(self.comissionPercent) * totalSells)

        return self.wage

    # Method that returns our character's attributes as a tuple so we can access
    # them without having to directly access the attributes in the class
    def getComissionedAttributes(self):
        return tuple(
            [self.name, self.address, self.jType, self.payMethod, self.isInSyndicate,
             self.syndicateCharge, self.serviceCharge, self.nextPayment, self.wage, None, None, self.sellCount]
        )

    # Method that constructs our class from the result of SELECT query in database
    def constructCommsFSelect(self, SelectResult):
        self.id = None
        self.name = SelectResult.name
        self.address = SelectResult.address
        self.jType = SelectResult.jType
        self.payType = SelectResult.payType
        self.payMethod = SelectResult.payMethod
        self.isInSyndicate = SelectResult.isInSyndicate
        self.syndicateCharge = SelectResult.syndicateCharge
        self.serviceCharge = SelectResult.serviceCharge
        self.nextPayment = SelectResult.nextPayment
        self.wage = int(SelectResult.wage)
        self.sellCount = SelectResult.sellCount
        self.saleId = None
        self.saleDate = None
        self.salePrice = None
        self.buyerName = None
        self.comissionPercent = SelectResult.comissionPercent
```

Refactored class and its subclasses:
```python
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
```
<br>
This was the refactoring applied in the project, until the next one.

![](https://media.giphy.com/media/Diym3aZO1dHzO/giphy.gif?cid=790b7611fc229e6da51519f4e1a37d07572544dc3f85fdd4&rid=giphy.gif&ct=g)

## References

[Refactor Guru](https://refactoring.guru/pt-br) <br>
Course classes and slides