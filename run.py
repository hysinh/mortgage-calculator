import gspread
from google.oauth2.service_account import Credentials
import math
#from PIL import Image, ImageFont, ImageDraw
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
import pyfiglet
from tabulate import tabulate
import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('mortgage_calculator')


mort_dict = {
  1 : {
    "principal" : 350000,
    "apr" : 4.3,
    "length_of_mortgage": 30,
    "monthly_payment": 1539.21,
    "lifetime_interest": 456345
  },
  2 : {
    "principal" : 350000,
    "apr" : 4.3,
    "length_of_mortgage": 30,
    "monthly_payment": 1539.21,
    "lifetime_interest": 456345
  },
  3 : {
    "principal" : 350000,
    "apr" : 4.3,
    "length_of_mortgage": 30,
    "monthly_payment": 1539.21,
    "lifetime_interest": 456345
  }
}

def clear():
    """
    Function to clear terminal through the game.
    """
    os.system("cls" if os.name == "nt" else "clear")


def welcome_screen():
    """
    ASCII PIXEL ART CODE
    """
    clear()
    logo_text = pyfiglet.figlet_format("Mortgage\nCalculator")
    print(logo_text)
    #cprint(figlet_format('mortgage tool', font='doom'),
    #    'yellow', 'on_blue', attrs=['bold'])
    print("Welcome to my Mortgage Comparison Tool")
    is_valid = False
    while is_valid != True:
        try:
            proceed = input("Would you like to use the mortgage calculator? y/n \n").lower()
            if proceed == "y":
                is_valid = True
            elif proceed == "n":
                is_valid = True
                print("*** Thanks for visiting! ***")
                exit()
            else:
                print("Please enter Y or N to proceed.")
        except ValueError:
            print("That is not a valid reponse. Please enter Y or N.")
    





def menu_screen():
    clear()
    print("\n\n")
    print("** Mortgage Calculator Tool **\n\n")
    print("You have the following options:\n ")
    table = [["Option",1,"Add a mortgage"],["Option",2,"View a mortgage"],
             ["Option",3,"View an amoritization schedule"],["Option",4,"Exit Program"]]
    print(tabulate(table))
    


def input_principal():
    """
    Checks Validation for principal input
    """
    is_valid = False
    while is_valid != True:
        try:
            principal = int(input('Enter the principal or loan amount: '))
            if principal > 0:
                is_valid = True
            else:
                print("Principal must be greater than 0. Please enter a valid number.")
        except ValueError:
            print("That is not a whole number. Please enter a valid number.")
        
    return principal


def input_apr():
    """
    Checks Validation for APR input
    """
    is_valid = False
    while is_valid != True:
        try:
            apr = float(input('Enter the Annual Percentage rate or APR (eg. 4.3): '))
            if apr > 0 and apr < 100:
                is_valid = True
            else:
                print("APR must be greater than 0. Please enter a valid number.")
        except ValueError:
            print("That is not a number. Please enter a valid number.")
        
    return apr


def input_loan_length():
    """
    Checks Validation for Mortgage Length input
    """
    is_valid = False
    while is_valid != True:
        try:
            length_of_mortgage = int(input('Enter the length of the mortgage in years (eg 30): '))
            if length_of_mortgage > 0:
                is_valid = True
            else:
                print("Your loan length must be greater than 0. Please enter a valid number.")
        except ValueError:
            print("That is not a number. Please enter a valid number.")
        
    return length_of_mortgage


class Mortgage:
    """
    Base Class for Mortgages
    """
    mortgage_ID = 0

    def __init__(self, principal, apr, length_of_mortgage):
        #instance attribute
        self.principal = principal
        self.apr = apr
        self.length_of_mortgage = length_of_mortgage
        Mortgage.mortgage_ID += 1
        self.mortgage_ID = Mortgage.mortgage_ID

    def details(self):
        """
        Method to return employee details as a string 
        """
        return f"\n\nMORTGAGE {self.mortgage_ID}:\nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years\nAnnual Percentage Rate: {self.apr}%"
    
    def calculate_monthly_payment(self):
        """
        Calculates monthly payment
        """
        monthly_payment = ((self.apr / 100 / 12) * self.principal) / (1 - (math.pow((1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12))))
        return f"Monthly payment = €{round(monthly_payment, 2)}"
    
    def calculate_lifetime_interest(self):
        pass

    def calculate_amoritization(self):
        pass



def compare_mortgages():
    print("inside the compare_mortgages function")


def create_mortgage():
    """
    Creates each Class Instance of a Mortgage - requires user input
    for the Principal amount, APR amount, and Length of Mortgage for
    caculations.
    """
    print("\n")
    principal = input_principal()
    apr = input_apr()
    length_of_mortgage = input_loan_length()

    mortgage1 = Mortgage(principal, apr, length_of_mortgage)
    print(mortgage1.details())
    print(mortgage1.calculate_monthly_payment()) 
    print(f"mortgage_id: {mortgage1.mortgage_ID}")

    return mortgage1
    

    new_mortgage = input("Type y/n if you would like to add another mortgage: ").lower()
    if new_mortgage == "y":
        principal2 = input_principal()
        apr2 = input_apr()
        length_of_mortgage2 = input_loan_length()
        mortgage2 = Mortgage(principal2, apr2, length_of_mortgage2)
        print(mortgage2.details())
        print(mortgage2.calculate_monthly_payment())
    else:
        print("Thanks for using the calculator")





def run_mortgage_tool():
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Please type in the number of your menu selection: "))
            if selection == 1:
                create_mortgage()
                #is_valid = True
            elif selection == 2:
                print("Option 2: View a particular mortgage.")
                is_valid = True
            elif selection == 3:
                print("Option 3: View an amorization schedule.")
                is_valid = True
            elif selection == 4:
                print("Option 4: Exit the program.")
                is_valid = True
            else:
                print("That is a not a valid option. Please type in a number between 1 - 4.")
        except ValueError:
            print("That is not a valid input. Please type in a number betwee 1 - 14.")    

if __name__ == '__main__':
    welcome_screen()
    menu_screen()
    run_mortgage_tool()
    



# ShowText = 'Python PIL'

# font = ImageFont.truetype('arialbd.ttf', 15) #load the font
# size = font.getsize(ShowText)  #calc the size of text in pixels
# image = Image.new('1', size, 1)  #create a b/w image
# draw = ImageDraw.Draw(image)
# draw.text((0, 0), ShowText, font=font) #render the text to the bitmap
# for rownum in range(size[1]): 
# #scan the bitmap:
# # print ' ' for black pixel and 
# # print '#' for white one
#     line = []
#     for colnum in range(size[0]):
#         if image.getpixel((colnum, rownum)): line.append(' '),
#         else: line.append('#'),
#     print(''.join(line))


