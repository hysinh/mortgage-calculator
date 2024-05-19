import gspread
from google.oauth2.service_account import Credentials
import math
import sys
from colorama import init
from termcolor import cprint
import pyfiglet
from tabulate import tabulate
import os
import pandas as pd

init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected

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


def clear_screen():
    """
    Function to clear terminal through the game.
    """
    os.system("cls" if os.name == "nt" else "clear")


def welcome_screen():
    """
    ASCII PIXEL ART CODE
    """
    clear_screen()
    logo_text = pyfiglet.figlet_format("Mortgage\nCalculator")
    print(logo_text)
    print("Welcome to my Mortgage Comparison Tool\n")
    proceed = input("Press the enter key to proceed \n").lower()

    # is_valid = False
    # while is_valid != True:
    #     try:
    #         proceed = input("Enter a key to proceed \n").lower()
    #         if proceed != "":
    #             is_valid = True
    #         else:
    #             print("Please enter a key and hit enter to proceed.")
    #     except ValueError:
    #         print("Not a valid reponse. Type a key and enter to proceed.")


MENU_OPTIONS = """
** Mortgage Calculator Tool **
You have the following options:
--------------------------------------------------------------
1. Add a mortgage               5. View Amortization Schedules
2. View a mortgage              6. Exit Program
3. Display Mortgage Comparison  7. Mortgage Metrics
4. Calculate Overpayments       
--------------------------------------------------------------

"""
def menu_screen():
    """
    Display Menu options
    """
    clear_screen()
    print(MENU_OPTIONS)


def validate_value(prompt_text):
    """
    Prompts user for input and validates that input is an integer greater
    than 0.
    """
    is_valid = False
    while is_valid != True:
        try:
            value = int(input(prompt_text))
            if value > 0:
                is_valid = True
            else:
                cprint("Invalid. Enter a whole number greater than 0", "red")
        except ValueError:
            cprint("That is not a number. Enter a whole number.", "red")
    return value


def validate_apr():
    """
    Prompts user for input and validates that the input is a float
    with a value between 0 and 100.
    """
    is_valid = False
    while is_valid != True:
        try:
            apr = float(input('Enter the Annual Percentage rate or APR (e.g. 4.3): \n'))
            if apr > 0 and apr < 100:
                is_valid = True
            else:
                cprint("APR must be greater than 0 but less than 100. Enter a valid APR.", "red")
        except ValueError:
            cprint("That is not a number. Enter a valid number.", "red")
    return apr


def validate_name(prompt_text):
    """
    Prompts user for input and validates that the input is a string of 10 characters or less
    """
    is_valid = False
    while is_valid != True:
        try:
            name = str(input(prompt_text))
            if len(name) > 0 and len(name) < 11:
                is_valid = True
            else:
                cprint("There is a maximum of 10 characters. Enter a valid name.", "red")
        except ValueError:
            cprint("That is not a valid entry. Enter a valid name.", "red")
    return name


class Mortgage:
    """
    Base Class for Mortgages - creates a mortgage class instance
    """
    mortgage_ID = 0
    start_year = 0 # start of mortgage
    extra_monthly_principal = 0
    updated_total_payments = 0

    def __init__(self, principal, apr, length_of_mortgage, mortgage_name):
        # instance attribute
        self.principal = principal
        self.apr = apr
        self.length_of_mortgage = length_of_mortgage
        self.mortgage_name = mortgage_name
        Mortgage.mortgage_ID += 1
        self.mortgage_ID = Mortgage.mortgage_ID
        self.start_year = Mortgage.start_year
        self.extra_monthly_principal = Mortgage.extra_monthly_principal
        self.updated_total_payments = Mortgage.updated_total_payments

    def details(self):
        return f"\nMORTGAGE: {self.mortgage_name} \nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years \nAnnual Percentage Rate: {self.apr}%"

    def calculate_monthly_payment(self):
        monthly_payment = round(((self.apr / 100 / 12) * self.principal) / (1 - (math.pow((1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12)))), 2)
        return monthly_payment
    
    def calculate_lifetime_interest(self):
        total_interest = round((self.length_of_mortgage * 12 * self.calculate_monthly_payment()) - self.principal, 2)
        return total_interest

    def get_table_values(self):
        # Creates mortgage values for comparison table
        row = [self.mortgage_ID,
            "€{:,.2f}".format(self.principal), 
            self.apr, 
            self.length_of_mortgage, 
            "€{:,.2f}".format(self.calculate_monthly_payment()), 
            "€{:,.2f}".format(self.calculate_lifetime_interest())
        ]
        return row

    def extra_principal_payments(self):
        updated_schedule = [["Mon.", "Payment", "Principal", "Xtra Princ", "Interest", "Balance"]]
        balance = self.principal
        rate = self.apr/100/12
        total_payments = self.length_of_mortgage*12
        monthly_payment = self.calculate_monthly_payment()
        extra_monthly_principal = self.extra_monthly_principal
        for Month in range(1, total_payments):
            interest_payment = balance * rate
            principal_payment = monthly_payment - interest_payment
            new_principal_payment = principal_payment + extra_monthly_principal
            balance -= new_principal_payment
            total_payments -= 1
            if balance > 0:
                updated_schedule.append([
                    Month,
                    "€{:,.2f}".format(monthly_payment),
                    "€{:,.2f}".format(principal_payment),
                    "€{:,.2f}".format(extra_monthly_principal),
                    "€{:,.2f}".format(interest_payment),
                    "€{:,.2f}".format(balance)
                ])
        return updated_schedule
    

    def calculate_amortization_schedule(self):
        schedule = [["Month", "Pmts Left", "Payment", "Principal", "Interest", "Balance"]]
        balance = self.principal
        rate = self.apr/100/12
        total_payments = self.length_of_mortgage*12
        monthly_payment = self.calculate_monthly_payment()
        for Month in range(1, total_payments):
            interest_payment = balance * rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            total_payments -= 1
            schedule.append([
                Month,
                total_payments,
                " €{:,.2f}".format(monthly_payment),
                " €{:,.2f}".format(principal_payment),
                " €{:,.2f}".format(interest_payment),
                " €{:,.2f}".format(balance)
            ])
        return schedule
    

    def create_mortgage_data(self):
        monthly_payment = self.calculate_monthly_payment()
        interest = self.calculate_lifetime_interest()
        data = [
            self.principal, 
            self.apr, 
            self.length_of_mortgage, 
            monthly_payment, 
            interest
        ]
        return data

    def update_mortgage_data(self):
        data = self.create_mortgage_data()
        mortgage_worksheet = SHEET.worksheet("mortgage_data")
        mortgage_worksheet.append_row(data)
        #mortgage_data = SHEET.worksheet("mortgage_data").get_all_values()
        #return mortgage_data

    def calculate_mortgage_metrics(self):
        """
        Calculate the average principal, APR, loan length, monthly payment, and 
        lifetime interest amount
        """
        mortgage_data = []
        mortgage_worksheet = SHEET.worksheet("mortgage_data").get_all_values()
        for column in mortgage_worksheet:
            avg = sum([int(y) for y in column])/(len(mortgage_worksheet))
            avg = math.ceil(avg)
            mortgage_data.append(avg)
        return mortgage_data


def display_mortgage_details(mortgage):
    print(mortgage.details())
    print("Monthly Payment: €{:,.2f}".format(mortgage.calculate_monthly_payment()))
    print("Cost of this loan: €{:,.2f}".format(mortgage.calculate_lifetime_interest()))
    print("\n")


def display_selected_mortgage(selection):
    for x in mortgage_dict:
        if selection == x:
                display_mortgage_details(mortgage_dict[x])
                is_valid = True
        else:
            continue


def adds_mortgage_instance_to_dict(mortgage):
    is_valid = False
    while is_valid != True:
        try:
            answer = str(input("\nWould you like to save this mortgage? Type Y or N \n")).lower()
            if answer == "y":
                mortgage_dict[mortgage.mortgage_ID] = mortgage
                cprint("Thanks. Your mortgage has been saved to your mortgages in this session.", "light_yellow")
                is_valid = True
            elif answer == "n":
                cprint("This mortgage was NOT SAVED to your mortgages in this session.", "red")
                break
            else:
                cprint("Please enter Y or N to proceed", "red")
        except ValueError:
            cprint("Please enter the number of the mortgage you want to select.", "red")


def create_mortgage():
    """
    Creates each Class Instance of a Mortgage - requires user input
    for the Principal amount, APR amount, and Length of Mortgage for
    calculations.
    """
    menu_screen()
    cprint("Enter Your Mortgage details in below:\n", "green")

    # Request input from the user
    mortgage_name = validate_name("Enter a name for this mortgage. You can use up to 10 characters. \n")
    principal = validate_value('Enter the principal or loan amount in Euro: \n')
    apr = validate_apr()
    length_of_mortgage = validate_value("Enter the length of the mortgage in years (e.g. 30): \n")

    # Creates a Mortgage Class Instance and adds it to the mortgage dictionary
    mortgage = Mortgage(principal, apr, length_of_mortgage, mortgage_name)

    # Creates a string of the mortgage data that appends to Google Sheets for future analysis
    mortgage.update_mortgage_data()
    #print(mortgage.create_mortgage_data())

    # Prints the Mortgage details just entered
    cprint("\nYou created a Mortgage with the following details:", "yellow")
    display_mortgage_details(mortgage)
    
    # Allows user to save mortgage for the session
    adds_mortgage_instance_to_dict(mortgage)

    print("\n*******************************************************\n")
    

def view_mortgage():
    """
    Allows user to view individual Mortgage details one at a time
    """
    menu_screen()

    # Prints a column of the available Mortgage Class Instances
    if len(mortgage_dict) == 0:
        cprint("This feature requires you to add at least one mortgage.\nAdd a mortgage to proceed.", "red")
    else:
        cprint("You have entered the following mortgages:\n", "green")
        for x in mortgage_dict:
            print(f"Mortgage: # {x}, {mortgage_dict[x].mortgage_name}")

        # Prompts user to select a mortgage to view or user can select to return to main menu
        print("\n")
        is_valid = False
        while is_valid != True:
            try:
                selection = int(input("Enter the number of the mortgage that you'd like to view \nor enter '0' to return to the main menu: \n"))
                if selection == 0:
                    menu_screen()
                    is_valid = True
                else:
                    display_selected_mortgage(selection)
                    cprint("(Enter 0 to view the Main menu)", "green")
            except ValueError:
                cprint("Please enter the number of the mortgage you want to select.", "red")

    print("\n*******************************************************\n")


def compare_mortgages():
    """
    Displays a comparison table of all the mortgages entered by the user
    """
    menu_screen()

    if len(mortgage_dict) < 2:
        cprint("This feature requires you to add at least two mortgage.\nAdd mortgages to proceed.", "red")
    else:
        mortgage_table = [["Mortgage","Principal","APR %","Loan\nLength","Monthly\nPayment", "Total\nInterest"]]

        cprint("\nMORTGAGE COMPARISON TABLE\n", "light_yellow")
        for x in mortgage_dict:
            mortgage_table.append(mortgage_dict[x].get_table_values())

        print(tabulate(mortgage_table, tablefmt="simple"))

    print("\n******************************************************* \n")


def extra_monthly_principal():
    """
    Calculates new payment and total interest with extra monthly principal payments
    """
    menu_screen()
    cprint("Calculate Mortgage Overpayments on an existing mortgage:\n", "green")

    mortgage_name = validate_name("Enter a name for this mortgage. You can use up to 10 characters. \n")
    principal = validate_value('Enter the remaining principal left on your existing loan in Euro: \n')
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value('How many years are left on your mortgage?  (e.g. 30) \n')

    extra_principal = validate_value('Enter the extra principal you would like to pay each month: \n')
    
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage, mortgage_name)
    #mortgage.update_mortgage_data()
    mortgage.extra_monthly_principal = extra_principal

    cprint("\nCurrent Mortgage: ", "light_yellow")
    display_mortgage_details(mortgage)
    
    print("\n**********************************************\n")
    cprint("UPDATED MORTGAGE AMORTIZATION SCHEDULE:", "light_yellow")

    print("Extra Monthly Principal Payment: €{:,.2f}".format(extra_principal), "\n")
    schedule = mortgage.extra_principal_payments()
    print(tabulate(schedule, headers="firstrow", tablefmt="github"))
    #print(schedule.to_string(index=False))

    adds_mortgage_instance_to_dict(mortgage)

    print("\n*******************************************************\n")


def lump_payment():
    """
    Calculates new payment and total interest with an extra lump principal payments
    """
    menu_screen()
    cprint("Calculate Mortgage Overpayments:\n", "green")

    mortgage_name = validate_name("Enter a name for this mortgage. You can use up to 10 characters. \n")
    principal = validate_value('Enter the remaining principal left on your loan in Euro: \n')
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value("Enter the remaining length of your mortgage in years: \n")

    lump_payment = validate_value('How much of a lump payment do you want to make? \n')
    
    # Creates Mortgage Instance with Current Mortgage inputs
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage, mortgage_name)

    # Prints Current Mortgage Details
    cprint("\nCurrent Mortgage: ----------------------------------------", "light_yellow")
    display_mortgage_details(mortgage)
    
    # Creates a new Mortgage Class Instance with the updated information
    cprint("\nUPDATED Mortgage: ----------------------------------------", "light_yellow")
    new_mortgage = Mortgage((principal-lump_payment), apr, remaining_length_of_mortgage, mortgage_name)
    #new_mortgage.update_mortgage_data() # Adds data to google sheets
    display_mortgage_details(new_mortgage)
    print(f"Principal Lump Overpayment: €{lump_payment}")

    adds_mortgage_instance_to_dict(new_mortgage)

    print("\n*******************************************************\n")


def overpayments():
    """
    Gives User the selection of making monthly overpayments or a lump sum overpayment
    """
    menu_screen()
    cprint("Mortgage Overpayments:\n", "green")

    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter 1 for Extra Monthly Principal overpayments, 2 for a Lump Principal overpayment, \nor enter '0' to exit this menu: \n"))
            if selection == 0:
                is_valid = True
            elif selection == 1:
                menu_screen()
                extra_monthly_principal()
            elif selection == 2:
                menu_screen()
                lump_payment()
            else:
               menu_screen()
               cprint("That is not a valid option. Please choose one from the list above.", "red")
        except ValueError:
            menu_screen()
            cprint("Please enter a valid mortgage number", "red")
    
    menu_screen()

    #print("\n*******************************************************")


def amortization():
    """
    Allows user to view an amoritization for individual Mortgage details one at a time
    """
    menu_screen()
    if len(mortgage_dict) == 0:
        cprint("This feature requires you to add at least one mortgage.\nAdd a mortgage to proceed.", "red")
    else:
        cprint("You have entered the following mortgages:\n", "green")
        for x in mortgage_dict:
            print(f"Mortgage: # {x}, {mortgage_dict[x].mortgage_name}")
        
        print("\n")
        is_valid = False
        while is_valid != True:
            try:
                selection = int(input("Enter the number of the mortgage that you'd like to amortize \nor enter '0' to return to the main menu: \n"))
                if selection == 0:
                    menu_screen()
                    is_valid = True
                else:
                    for x in mortgage_dict:
                        if selection == x:
                            clear_screen()
                            cprint(f"\n\nAMORTIZATION SCHEDULE FOR:", "yellow")
                            schedule = mortgage_dict[x].calculate_amortization_schedule()
                            display_mortgage_details(mortgage_dict[x])
                            print(tabulate(schedule, headers="firstrow", tablefmt="github"))
                            print("\n")
                            is_valid = True
                        else:
                            continue
            except ValueError:
                print("Please enter a correct number")

    print("\n*******************************************************\n")

    
def print_mortgage_avg():
    """
    Prints the Mortgage data averages in a table
    """

    menu_screen()
    if len(mortgage_dict) == 0:
        cprint("This feature requires you to add at least one mortgage.\nAdd a mortgage to proceed.", "red")
    else:
        cprint("The Mortgage Averages collected:\n", "green")
        table = [
            ['Principal', 'APR', 'Loan Length', 'Monthly Payment', 'Total Interest'],
            ['350000', '4.3', '19', '2249.22', '162826.16'],
            ['350000', '4.3', '19', '2249.22', '162822.16'],
            ['350000', '4.3', '19', '2249.22', '162822.16']
            ]

        print(tabulate(table))
    
    print("\n*******************************************************")


def run_mortgage_tool():
    """
    Allows the user to select from various menu options for the Mortgage Comparison Tool
    """
    menu_screen()
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter a selection from the Main Menu: \n"))
            if selection == 1:
                create_mortgage()
                cprint("(Enter 0 to view the Main menu)", "green")
            elif selection == 2:
                view_mortgage()
                cprint("(Enter 0 to view the Main menu)", "green")
            elif selection == 3:
                compare_mortgages()
                cprint("(Enter 0 to view the Main menu)", "green")
            elif selection == 4:
                overpayments()
                cprint("(Enter 0 to view the Main menu)", "green")
            elif selection == 5:
                amortization()
                cprint("(Enter 0 to view the Main menu)", "green")
            elif selection == 6:
                clear_screen()
                print("\n\nThanks for using the Mortgage Comparison Tool.\n")
                is_valid = True
            elif selection ==7:
                print("Mortgage Metrics Table")
                cprint("(Enter 0 to view the Main menu)", "green")
            elif selection == 0:
                menu_screen()
            else:
                cprint("That is not a menu option. Type in a number between 1 - 7 or 0 for the main menu.", "red")
        except ValueError:
            cprint("That is not a valid input. Please type in a number between 1 - 7 or 0.", "red")


if __name__ == '__main__':
    welcome_screen()
    run_mortgage_tool()
    




