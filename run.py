import gspread
from google.oauth2.service_account import Credentials
import math

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mortgage_calculator')



"""
Mortgage Calculator / Comparison Tool:
Enter your mortgage(loan) amount, the APR (Annual Percentage Rate), and the length of
the loan to compare monthly payments and how much interest you pay over the lifetime of 
the loan.

# Principal = int(loan/mortgage amount)
# APR = float(Annual percentage rate as a percentage - 4.5%)
# loan_length = int(length of the loan in years - eg 15, 20, 30 , etc)

Users can input up to 4 sets of loan data.

# add new mortgage (creates a new class instance)
# delete/remove mortgage 
# save mortgage(s) (writes to my google sheet - removes class references)
# load mortgages (retrieve from google sheets - adds classes references)
# set active mortgage
# list mortgage
# everything is an Class instance operated on that mortgage

Program calculates:
1. Monthly_loan_payment = float(number with two decimal placements)
2. total_interest = float(total interest paid over the lifetime of the loan)
3. Difference in interest between different loans

# interest paid (# of months into mortgage)
# How much interest / principal paid in year (input year eg 12)
# amortization schedule
# if i pay XX, how much does it shorten the mortgage

Program displays a table:
1. Principal Amount
2. APR
3. loan_length
4. Monthly_loan_payment
5. total_interest paid over the course of the loan
6. how much money you save in interest with each reduction in total loan_length

Program requests if the user would like to run the program again to create new inputs and comparisons.

"""

class Mortgage:
    """
    Base Class for Mortgages
    """
    mortgage_no = 0

    def __init__(self):
        #instance attribute
        self.principal = int(input('Enter the principal or loan amount:'))
        self.apr = float(input('Enter the Annual Percentage rate (eg. 4.3):'))
        self.length_of_mortgage = int(input('Enter the length of the mortgage in years (eg 30):'))
        Mortgage.mortgage_no += 1
        self.mortgage_no = Mortgage.mortgage_no

    def details(self):
        """
        Method to return employee details as a string 
        """
        return f"Principal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years\nAnnual Percentage Rate: {self.apr}%"
    
    def calculate_monthly_payment(self):
        """
        Calculates monthly payment
        """
        monthly_payment = ((self.apr / 100 / 12) * self.principal) / (1 - (math.pow((1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12))))
        return f"Monthly payment = €{round(monthly_payment, 2)}"




def compare_mortgages():
    print("inside the compare_mortgages function")

print("Welcome to my Mortgage Comparison Tool")
compare_mortgages()

mortgage1 = Mortgage()

print(mortgage1.details())
print(mortgage1.calculate_monthly_payment())


