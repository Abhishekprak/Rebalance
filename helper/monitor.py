

async def NS_N50_Momentum():
    # Example code
    return "NS_N50_Momentum result"

async def NS_Focused_Growth():
    # Example code
    return "NS_Focused_Growth result"

async def GOLD():
    # Example code
    return "GOLD result"

async def SILVER():
    # Example code
    return "SILVER result"

async def NS_Low_Volatility():
    # Example code
    return "NS_Low_Volatility result"

async def NS_N500_Momentum():
    # Example code
    return "NS_N500_Momentum result"

async def Gilt():
    # Example code
    return "Gilt result"

async def NS_Flexicap_Value():
    # Example code
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