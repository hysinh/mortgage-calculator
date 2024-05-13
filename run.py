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


mortgage_dict = {}

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
    print("Welcome to my Mortgage Comparison Tool")
    is_valid = False
    while is_valid != True:
        try:
            proceed = input("Enter any key to proceed \n").lower()
            if proceed != "":
                is_valid = True
            # elif proceed == "n":
            #     is_valid = True
            #     print("*** Thanks for visiting! ***")
            #     exit()
            else:
                print("Please enter any letter to proceed.")
        except ValueError:
            print("That is not a valid reponse. Please enter Y or N.")
    


def menu_screen():
    """
    Menu Screen with options displayed in a table
    """
    clear()
    print("\n")
    print("** Mortgage Calculator Tool **\n")
    print("You have the following options:\n ")
    table = [
        ["Option",1,"Add a mortgage"],
        ["Option",2,"View a Mortgage"],
        ["Option",3,"Display Mortgage Comparison"],
        ["Option",4,"Make Extra Payments"],
        ["Option",5,"Exit Program"],
        ["Option",0,"Return to Main Menu"]]
    print(tabulate(table))
    print("\n")
    

def small_menu():
    """
    Compressed Menu that in a single line 
    """
    print("** Mortgage Calculator Tool MENU OPTIONS **")
    print("1. Add Mortgage | 2. View a Mortgage | 3. Display Mortgage Comparison")
    print("4. Make Extra Payments | 5. Exit Program | 0. Return to Main Menu | ")
    print("\n*******************************************************")


def input_principal():
    """
    Checks Validation for principal input
    """
    is_valid = False
    while is_valid != True:
        try:
            principal = int(input('Enter the principal or loan amount in Euro: \n'))
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
            apr = float(input('Enter the Annual Percentage rate or APR (e.g. 4.3): \n'))
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
            length_of_mortgage = int(input('Enter the length of the mortgage in years (e.g. 30): \n'))
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
    mortgage_ID = 200

    dict = {}

    def __init__(self, principal, apr, length_of_mortgage):
        #instance attribute
        self.principal = principal
        self.apr = apr
        self.length_of_mortgage = length_of_mortgage
        Mortgage.mortgage_ID += 1
        self.mortgage_ID = Mortgage.mortgage_ID
        self.dict = Mortgage.dict

    def details(self):
        """
        Method to return employee details as a string 
        """
        return f"\nMORTGAGE {self.mortgage_ID}:\nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years\nAnnual Percentage Rate: {self.apr}%"
    
    def calculate_monthly_payment(self):
        """
        Calculates monthly payment
        """
        monthly_payment = round(((self.apr / 100 / 12) * self.principal) / (1 - (math.pow((1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12)))), 2)
        return monthly_payment
    
    def append_dict(self):
        self.dict.update([(self.mortgage_ID, {"principal": self.principal, "apr": self.apr, "length_of_mortgage": self.length_of_mortgage})])
        mortgage_dict.update(self.dict)
    
    def calculate_lifetime_interest(self):
        total_interest = round((self.length_of_mortgage * 12 * self.calculate_monthly_payment()) - self.principal, 2)
        return total_interest

    def get_table_values(self):
        row = [self.mortgage_ID, "€{:,.2f}".format(self.principal), self.apr, self.length_of_mortgage, "€{:,.2f}".format(self.calculate_monthly_payment()), "€{:,.2f}".format(self.calculate_lifetime_interest())]
        return row
    
    def calculate_amoritization(self):
        pass


# mixin ExtraPrincipal:
#     pass


def create_mortgage():
    """
    Creates each Class Instance of a Mortgage - requires user input
    for the Principal amount, APR amount, and Length of Mortgage for
    caculations.
    """
    clear()
    small_menu()
    print("\nEnter Your Mortgage details in below:\n")
    principal = input_principal()
    apr = input_apr()
    length_of_mortgage = input_loan_length()

    mortgage = Mortgage(principal, apr, length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage
    print("\nYou created a Mortgage with the following details:")
    print(mortgage.details())
    print("Your monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment())) 
    #print(f"mortgage_id: {mortgage.mortgage_ID}")
    print("\n*******************************************************\n")
    return mortgage
    
def view_mortgage():
    """
    Allows user to view individual Mortgage details one at a time
    """
    clear()
    small_menu()
    print("You have entered the following mortgages:\n")
    for x in mortgage_dict:
        print(f"Mortgage: {x}")

    print("\n")
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter the number of the mortgage that you'd like to view \nor enter '0' to return to the main menu: \n"))
            if selection == 0:
                menu_screen()
                is_valid = True
            else:
                for x in mortgage_dict:
                    if selection == x:
                        print(mortgage_dict[x].details())
                        print(f"Monthly payment = €{mortgage_dict[x].calculate_monthly_payment()}")
                        print(f"Cost of this loan = €{mortgage_dict[x].calculate_lifetime_interest()})")
                        is_valid = True
                    else:
                        continue
                        #print("Sorry. That is not an available mortgage. Please choose one from the list above.")
                        #is_valid = True
        except ValueError:
            print("Please enter a correct number")

    print("\n*******************************************************\n")
        


def compare_mortgages():
    """
    Creates a table to compare mortgages
    """
    clear()
    small_menu()
    mortgage_table = [["Mortgage","Principal","APR %","Loan\nLength","Monthly\nPayment", "Total\nInterest", "Total\nSavings"]]

    print("\nMORTGAGE COMPARISON TABLE\n")
    for x in mortgage_dict:
        #print(mortgage_dict[x].details())
        #print(f"Monthly payment = €{mortgage_dict[x].calculate_monthly_payment()}")
        mortgage_table.append(mortgage_dict[x].get_table_values())

    print(tabulate(mortgage_table, tablefmt="simple"))
    print("\n******************************************************* \n")
    

def extra_monthly_principal():
    """
    Calculates new payment and total interest with extra monthly principal payments
    """
    clear()
    small_menu()
    print("You have entered the following mortgages:\n")
    for x in mortgage_dict:
        print(f"Mortgage: {x}")
    
    print("\n")
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter the number of the mortgage that you'd like to view \nor enter '0' to return to the main menu: \n"))
            if selection == 0:
                menu_screen()
                is_valid = True
            else:
                for x in mortgage_dict:
                    if selection == x:
                        extra_principal = int(input("Enter the amount of extra principal you want to pay each month: \n"))
                        new_payment = extra_principal + mortgage_dict[x].calculate_monthly_payment()
                        print("New Principal payment", new_payment)
                        print(mortgage_dict[x].details())
                        print(f"Monthly payment = €{mortgage_dict[x].calculate_monthly_payment()}")
                        print(f"Cost of this loan = €{mortgage_dict[x].calculate_lifetime_interest()}")
                        continue
                    else:
                        continue
                        #print("Sorry. That is not an available mortgage. Please choose one from the list above.")
                        #is_valid = True
        except ValueError:
            print("Please enter a correct number")


    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter the amount of extra principal you want to pay each month: \n"))
            for x in mortgage_dict:
                if selection == x:
                    new_payment = round(((mortgage_dict[x].apr / 100 / 12) * mortgage_dict[x].principal) / (1 - (math.pow((1 + (mortgage_dict[x].apr / 100 / 12)), (-mortgage_dict[x].length_of_mortgage * 12)))), 2)
                    print(f"New Payment Amount: {new_payment}")
                    print(f"Monthly payment = €{mortgage_dict[x].calculate_monthly_payment()}")
                    print(f"Cost of this loan = €{mortgage_dict[x].calculate_lifetime_interest()})")
                    is_valid = True
                else:
                    continue
                    #is_valid = True
        except ValueError:
            print("Please enter a whole number.")

    print("\n*******************************************************\n")


    #interest = (monthly+extra amount) * totalpayments - principal


def run_mortgage_tool():
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter a menu selection: \n"))
            if selection == 1:
                create_mortgage()
                #is_valid = True
            elif selection == 2:
                view_mortgage()
                print("\n")
                #print(mortgage_dict[1].calculate_monthly_payment())
                #print("Option 2: View a particular mortgage.")
                #is_valid = True
            elif selection == 3:
                compare_mortgages()
                #is_valid = True
            elif selection == 4:
                extra_monthly_principal()
                #is_valid = True
            elif selection == 5:
                print("Option 5: Exit the program.")
                is_valid = True
            elif selection == 0:
                menu_screen()
            else:
                print("That is a not a valid option. Please type in a number between 1 - 4.")
        except ValueError:
            print("That is not a valid input. Please type in a number betwee 1 - 14.")    

if __name__ == '__main__':
    welcome_screen()
    menu_screen()
    run_mortgage_tool()
    #print(f"Mort_dict: {mort_dict}")
    



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


