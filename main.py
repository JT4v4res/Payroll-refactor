from classes import sqlmanager, system_postings
import uuid
import datetime as dt

sqlmanager.Base.metadata.create_all(sqlmanager.engine)

def dynamic_insert(id, name, address, j_type, payType, payMethod, isInSyndicate, tax, serviceCharge,
                   date, wage, pointCardId, workedHours, sellCount, commissionPercent):
    emp_mgr.insert(
        sqlmanager.Employee(id, name, address, j_type, payType, payMethod, isInSyndicate, tax, serviceCharge,
                            date, wage, pointCardId, workedHours, sellCount, commissionPercent)
    )


if __name__ == '__main__':
    emp_mgr = sqlmanager.EmployeeManager()
    sales_mgr = sqlmanager.SalesManager()
    syndicate_mgr = sqlmanager.SyndicateManager()
    sch_mgr = sqlmanager.SchManager()

    jTypes = {"hourly": "hourly wage", "salaried": "monthly salary", "commissioned": "commission"}

    while True:
        print("Welcome to Payroll System")
        print("Please, select an action")
        print("----------------------------")
        print("1 - Add a new employee")
        print("2 - Remove an employee")
        print("3 - Beat time")
        print("4 - Launch new sale")
        print("5 - Launch service charge")
        print("6 - Update employee record")
        print("7 - Make today\'s payments")
        print("8 - Personalized schedules")
        print("11 - EXIT")
        print("----------------------------")
        x = int(input('Enter your option: '))
        if x == 1:
            name = input('Enter the employee\'s name: ')
            address = input('Enter the employee\'s address: ')
            isInSyndicate = input('Syndicate: True or False: ')
            if isInSyndicate.lower() == 'true':
                isInSyndicate = True
            else:
                isInSyndicate = False
            wage = input('Employee\'s wage: ')
            print("----------------------------")
            print("----- Summary of jobs ------")
            print("---------- Hourly ----------")
            print("--------- Salaried ---------")
            print("------- Commissioned -------")
            print("----------------------------")
            j_type = input('Enter the employee\'s job: ')
            tax = 0
            if isInSyndicate:
                tax = input('Enter the syndicate charge: ')
                syndicate_mgr.insert(sqlmanager.Syndicate(
                    None, name, address, tax, 0
                ))

            payMethod = input('Choose your paymethod between: \n 1.Check by mail\n 2.Check in hand\n 3.Account deposit\n opt:')

            if j_type.lower() == 'hourly':
                dynamic_insert(None, name, address, j_type.lower(), 'hourly wage', payMethod, isInSyndicate, tax, 0,
                                dt.date.today() + dt.timedelta(7), wage, str(uuid.uuid4()), 0, None, None)
            elif j_type.lower() == 'salaried':
                dynamic_insert(None, name, address, j_type.lower(), 'monthly salary', payMethod, isInSyndicate, tax, 0,
                                dt.date.today() + dt.timedelta(30), wage, None, None, None, None)
            elif j_type.lower() == 'commissioned':
                percentComm = input('Enter the percentual of commission: ')
                dynamic_insert(None, name, address, j_type.lower(), 'commission', payMethod, isInSyndicate, tax, 0,
                                dt.date.today() + dt.timedelta(15), wage, None, None, 0, percentComm)
        elif x == 2:
            name = input('Enter the name of the employee to be removed: ')
            emp_mgr.delete(name)
            syndicate_mgr.delete(name)
        elif x == 3:
            name = input('Enter your name: ')
            point_card = system_postings.PointCard()
            point_card.construct_by_select(emp_mgr.search(name))

            arrival = int(input('Enter your time of entry: '))
            departure = int(input('Enter your departure time: '))

            emp_mgr.update(getattr(point_card, "name"), point_card.post_point_card(arrival, departure), "workedHours")
        elif x == 4:
            name = input('Enter your name: ')
            new_sale = system_postings.SalePost()
            new_sale.construct_by_select(emp_mgr.search(name))

            bName = input('Buyer name: ')
            price = input('Sell price: ')

            new_sale.get_sale(bName, price)
            sTup = new_sale.post_new_sale()

            emp_mgr.update(getattr(new_sale, "name"), new_sale.get_sell_count(), "sellCount")
            sales_mgr.insert(sqlmanager.Sales(sTup[0], sTup[1], sTup[2],
                                              sTup[3], sTup[4], 0))
        elif x == 5:
            name = input('Enter employee\'s name: ')
            charge = input('Enter the service charge: ')

            emp_mgr.update(name, charge, "serviceCharge")
            syndicate_mgr.update(name, charge, "serviceCharge")
        elif x == 6:
            e_name = input('Enter your name: ')
            print("----------------------------")
            print("---- Summary of Updates ----")
            print("------- 1 - Address  -------")
            print("--------- 2 - Type ---------")
            print("--------- 3 - Name ---------")
            print("------ 4 - Syndicate -------")
            print("--- 5 - Syndicate Charge ---")
            print("---- 6 - Payment method ----")
            print("----------------------------")
            y = int(input('Enter option: '))
            if y == 1:
                n_addr = input('Enter new address: ')
                emp_mgr.update(e_name, n_addr, "address")
            elif y == 2:
                n_type = input('Enter new type: ')
                emp_mgr.update(e_name, n_type, "jType")
                emp_mgr.update(e_name, jTypes[n_type], "payType")
                if n_type.lower() == "commissioned":
                    com_tax = float(input('Enter the commission percent: '))
                    emp_mgr.update_type(e_name, com_tax, 0)
                elif n_type.lower() == "hourly":
                    emp_mgr.update_type(e_name, None, None, 0, str(uuid.uuid4()))
                elif n_type.lower() == "salaried":
                    emp_mgr.update_type(e_name, None, None, None, None)
            elif y == 3:
                n_name = input('Enter new name: ')
                emp_mgr.update(e_name, n_name, "name")
                syndicate_mgr.update(e_name, n_name, "name")
            elif y == 4:
                n_syndicate = input('Syndicate True or False: ')
                name = input('Enter your name: ')
                if n_syndicate.lower() == 'true':
                    address = input('Enter you address: ')
                    tax = input('Enter tax: ')
                    syndicate_mgr.insert(sqlmanager.Syndicate(
                        None, name, address, tax, 0
                    ))
                    emp_mgr.update(name, 1, "isInSyndicate")
                else:
                    syndicate_mgr.delete(name)
                    emp_mgr.update(name, 0, "isInSyndicate")
                    emp_mgr.update(name, 0, "syndicateCharge")
            elif y == 5:
                charge = input('Enter syndicate charge: ')
                emp_mgr.update(e_name, charge, "syndicateCharge")
                syndicate_mgr.update(e_name, charge, "syndicateCharge")
            elif y == 6:
                print('------------------------')
                print("Table of week days")
                print("0 - Monday")
                print("1 - Tuesday")
                print("2 - Wednessday")
                print("3 - Thursday")
                print("4 - Friday")
                print('------------------------')
                name = input('Enter your name: ')
                dCode = int(input('Enter the day of payment on schedule: '))
                newPaySched = input('Enter the new payment schedule description: ').lower()
                sch_mgr.insert(sqlmanager.PersoSchedule(None, dCode, newPaySched))
                if newPaySched == 'monday':
                    emp_mgr.update(name, 'monday', "payType")
                elif newPaySched == 'tuesday':
                    emp_mgr.update(name, 'tuesday', "payType")
                elif newPaySched == 'wednessday':
                    emp_mgr.update(name, 'wednessday', "payType")
                elif newPaySched == 'thursday':
                    emp_mgr.update(name, 'thursday', "payType")
                elif newPaySched == 'friday':
                    emp_mgr.update(name, 'friday', "payType")
        elif x == 7:
            print('------------------------')
            print('1.Pay today\'s employees')
            print('2.Pay in a given period')
            print('------------------------')

            z = int(input('option: '))
            if z == 1:
                weekly = system_postings.WeeklySchedule()
                weekly.do_payment()
                weekly.do_payment()
                TwoWeekly = system_postings.TwoWeeklySchedule()
                TwoWeekly.do_payment()
                monthly = system_postings.MonthlySchedule()
                monthly.do_payment()
            else:
                days = int(input('Enter period: '))
                weekly = system_postings.WeeklySchedule()
                weekly.do_payment(days)
                weekly.do_payment(days, 1)
                TwoWeekly = system_postings.TwoWeeklySchedule()
                TwoWeekly.do_payment(days)
                monthly = system_postings.MonthlySchedule()
                monthly.do_payment(days)
        elif x == 8:
            print('------------------------')
            print("Table of week days")
            print("0 - Monday")
            print("1 - Tuesday")
            print("2 - Wednessday")
            print("3 - Thursday")
            print("4 - Friday")
            print('------------------------')
            name = input('Enter your name: ')
            dCode = int(input('Enter the day of payment on schedule: '))
            newPaySched = input('Enter the new payment schedule description: ').lower()
            sch_mgr.insert(sqlmanager.PersoSchedule(None, dCode, newPaySched))
            if newPaySched == 'monday':
                emp_mgr.update(name, 'monday', "payType")
            elif newPaySched == 'tuesday':
                emp_mgr.update(name, 'tuesday', "payType")
            elif newPaySched == 'wednessday':
                emp_mgr.update(name, 'wednessday', "payType")
            elif newPaySched == 'thursday':
                emp_mgr.update(name, 'thursday', "payType")
            elif newPaySched == 'friday':
                emp_mgr.update(name, 'friday', "payType")
        else:
            break
