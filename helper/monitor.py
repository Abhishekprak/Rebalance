# from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

def first_monday(year, month):
    first_day = datetime(year, month, 1)
    first_monday = first_day + timedelta(days=(7 - first_day.weekday() % 7))
    return first_monday

async def NS_N50_Momentum():
    return "NS_N50_Momentum result"

async def NS_Focused_Growth():
    # Example code
    current_date = datetime.now().day
    today = datetime.now()
    if current_date == 15:
        next_month_15th = today + relativedelta(months=1)
        next_month_15th = next_month_15th.replace(day=15)
        print(next_month_15th)
        pass
    return "NS_Focused_Growth result"

async def GOLD():
    # Example code
    return "GOLD result"

async def SILVER():
    # Example code
    return "SILVER result"

async def NS_Low_Volatility():
    today = datetime.now()
    if today.weekday() == 0 and 1 <= today.day <= 7:
        print("Today is the first Monday of the month.")
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        next_first_monday = first_monday(next_year, next_month)
        print("Next first Monday:", next_first_monday)
    return "NS_Low_Volatility result"

async def NS_N500_Momentum():
    # Example code
    return "NS_N500_Momentum result"

async def Gilt():
    today = datetime.now()
    if today.weekday() == 0 and 1 <= today.day <= 7:
        print("Today is the first Monday of the month.")
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        next_first_monday = first_monday(next_year, next_month)
        print("Next first Monday:", next_first_monday)
    return "Gilt result"

async def NS_Flexicap_Value():
    current_date = datetime.now().day
    today = datetime.now()
    if current_date == 1:
        next_month_1th = today + relativedelta(months=1)
        next_month_1th = next_month_1th.replace(day=1)
        print(next_month_1th)
    return "NS_Flexicap_Value result"

async def NS_N200_Momentum():
    # Example code
    return "NS_N200_Momentum result"


"""
from datetime import datetime, timedelta

def get_nth_weekday_of_month(year, month, weekday, n):
    # weekday: Monday=0, Sunday=6
    first_day = datetime(year, month, 1)
    # Find the first occurrence of the weekday
    first_occurrence = first_day + timedelta(days=(weekday - first_day.weekday() + 7) % 7)
    # Calculate the nth occurrence
    nth_occurrence = first_occurrence + timedelta(weeks=n - 1)
    return nth_occurrence

def is_today_4th_monday():
    today = datetime.today()
    fourth_monday = get_nth_weekday_of_month(today.year, today.month, weekday=0, n=4)
    return today.date() == fourth_monday.date()

def next_month_4th_monday():
    today = datetime.today()
    next_month = today.month + 1 if today.month < 12 else 1
    next_year = today.year + 1 if today.month == 12 else today.year
    return get_nth_weekday_of_month(next_year, next_month, weekday=0, n=4)

# Example usage
if is_today_4th_monday():
    print("Today is the 4th Monday of the month!")
    print("The 4th Monday of next month is:", next_month_4th_monday().strftime("%Y-%m-%d"))
else:
    print("Today is not the 4th Monday of the month.")

"""