import datetime
import calendar

def Expiry_dates(start, end, day):
    list_exp_dates = list()
    expiry_day="Thursday"
    start_date=datetime.date.today().strftime("%d/%m/%Y")
    end_date=datetime.date(datetime.date.today().year, 12, 31).strftime("%d/%m/%Y")

    # start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
    # end_date = datetime.datetime.strptime(end, '%d/%m/%Y')

    for i in range((end_date - start_date).days):
        if calendar.day_name[(start_date + datetime.timedelta(days=i + 1)).weekday()] == expiry_day:
            # print((start_date + datetime.timedelta(days=i + 1)).strftime("%d%b%Y"))
            list_exp_dates.append((start_date + datetime.timedelta(days=i + 1)).strftime("%d%b%Y"))
    print("Printing list :" , list_exp_dates)
    return list_exp_dates

# weekday_count("01/01/2022", "31/01/2017", "Thursday")

weekday_count(datetime.date.today().strftime("%d/%m/%Y"), datetime.date(datetime.date.today().year, 12, 31).strftime("%d/%m/%Y"), "Thursday")
last_year = datetime.date(datetime.date.today().year, 12, 31).strftime("%d/%m/%Y")
print(last_year)
