import gspread
from google.oauth2.service_account import Credentials
import math
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
import pyfiglet
from tabulate import tabulate
import os
import pandas as pd

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
            proceed = input("Enter a key to proceed \n").lower()
            if proceed != "":
                is_valid = True
            else:
                print("Please enter a key and hit enter to proceed.")
        except ValueError:
            print("Not a valid reponse. Type a key and enter to proceed.")


def menu_screen():
    """
    Menu Screen with options displayed in a table
    """
    clear()
    print("** Mortgage Calculator Tool **\n")
    print("You have the following options:\n ")
    table = [
        [1, "Add a mortgage", 5, "View Amortization Schedules"],
        [2, "View a Mortgage", 6, "Exit Program"],
        [3, "Display Mortgage Comparison", 7, "Mortgage Metrics"],
        [4, "Calculate Overpayments", 0, "Return to Main Menu"],
    ]
    print(tabulate(table))
    print("\n*******************************************************")


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
            cprint("Invalid. Please enter a valid number.", "red")
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
                cprint("APR must be greater than 0 but less than 100. Please enter a valid number.", "red")
        except ValueError:
            cprint("That is not a number. Please enter a valid number.", "red")
    return apr


class Mortgage:
    """
    Base Class for Mortgages - creates a mortgage class instance
    """
    mortgage_ID = 0
    start_year = 0 # start of mortgage
    extra_monthly_principal = 0
    updated_total_payments = 0

    def __init__(self, principal, apr, length_of_mortgage):
        # instance attribute
        self.principal = principal
        self.apr = apr
        self.length_of_mortgage = length_of_mortgage
        Mortgage.mortgage_ID += 1
        self.mortgage_ID = Mortgage.mortgage_ID
        self.start_year = Mortgage.start_year
        self.extra_monthly_principal = Mortgage.extra_monthly_principal
        self.updated_total_payments = Mortgage.updated_total_payments

    def details(self):
        return f"\nMORTGAGE {self.mortgage_ID}: \nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years \nAnnual Percentage Rate: {self.apr}%"

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
        updated_schedule = []
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
                updated_schedule.append({
                        'Month #' : Month,
                        'Payments Left' : total_payments,
                        'Payment' : "€{:,.2f}".format(monthly_payment),
                        'Principal' : "€{:,.2f}".format(principal_payment),
                        'Extra Principal' : "€{:,.2f}".format(extra_monthly_principal),
                        'Interest' : "€{:,.2f}".format(interest_payment),
                        'Balance' : "€{:,.2f}".format(balance)     
                })
        return pd.DataFrame(updated_schedule, index=None)

    def calculate_amortization_schedule(self):
        schedule = []
        balance = self.principal
        rate = self.apr/100/12
        total_payments = self.length_of_mortgage*12
        monthly_payment = self.calculate_monthly_payment()
        for Month in range(1, total_payments):
            interest_payment = balance * rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            total_payments -= 1
            schedule.append({
                    'Month #' :  Month,
                    'Payments Left' :  total_payments,
                    'Payment' : " €{:,.2f}".format(monthly_payment),
                    'Principal' : " €{:,.2f}".format(principal_payment),
                    'Interest' : " €{:,.2f}".format(interest_payment),
                    'Balance' : " €{:,.2f}".format(balance)     
                })
        return pd.DataFrame(schedule, index=None)

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

# def update_mortgage_data(Mortgage):
#     data = Mortgage.create_mortgage_data()
#     print(data)
    #mortgage_worksheet = SHEET.worksheet("mortgage_data")
    #mortgage_worksheet.append_row(data)
    #print(mortgage_worksheet)


def create_mortgage():
    """
    Creates each Class Instance of a Mortgage - requires user input
    for the Principal amount, APR amount, and Length of Mortgage for
    calculations.
    """
    menu_screen()
    cprint("\nEnter Your Mortgage details in below:\n", "green")

    # Request input from the user
    principal = validate_value('Enter the principal or loan amount in Euro: \n')
    apr = validate_apr()
    length_of_mortgage = validate_value("Enter the length of the mortgage in years (e.g. 30): \n")

    # Creates a Mortgage Class Instance
    mortgage = Mortgage(principal, apr, length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage
    #mortgage.create_mortgage_data()
    print(mortgage.create_mortgage_data())

    # Prints the Mortgage details just entered
    cprint("\nYou created a Mortgage with the following details:", "yellow")
    print(mortgage.details())
    print("Your monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment())) 

    print("\n*******************************************************\n")
    

def view_mortgage():
    """
    Allows user to view individual Mortgage details one at a time
    """
    menu_screen()

    # Prints a column of the available Mortgage Class Instances
    if len(mortgage_dict) == 0:
        cprint("This feature requires you to add at least one mortgage. Add a mortgage to proceed.", "red")
    else:
        cprint("You have entered the following mortgages:\n", "green")
        for x in mortgage_dict:
            print(f"Mortgage: {x}")

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
                    for x in mortgage_dict:
                        if selection == x:
                            print(mortgage_dict[x].details())
                            print("Monthly Payment: €{:,.2f}".format(mortgage_dict[x].calculate_monthly_payment()))
                            print("Cost of this loan: €{:,.2f}".format(mortgage_dict[x].calculate_lifetime_interest()))
                            is_valid = True
                        else:
                            #cprint("That is not an available mortgage. Please enter a mortgage number from the list.", "red")
                            continue
            except ValueError:
                cprint("Please enter a valid number", "red")


def compare_mortgages():
    """
    Displays a comparison table of all the mortgages entered by the user
    """
    menu_screen()

    if len(mortgage_dict) < 2:
        cprint("This feature requires you to add at least two mortgage. Add mortgages to proceed.", "red")
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

    principal = validate_value('Enter the remaining principal left on your existing loan in Euro: \n')
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value('How many years are left on your mortgage?  (e.g. 30) \n')

    extra_principal = validate_value('Enter the extra principal you would like to pay each month: \n')
    
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage
    #mortgage.update_mortgage_data()
    mortgage.extra_monthly_principal = extra_principal
    updated_total_payments = mortgage.updated_total_payments

    cprint("\nCurrent Mortgage: ", "light_yellow")
    print(mortgage.details())
    print("Your current monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment()))
    
    print("\n**********************************************\n")
    cprint("UPDATED MORTGAGE AMORTIZATION SCHEDULE:", "light_yellow")
    
    print("Extra Monthly Principal Payment: €{:,.2f}".format(extra_principal))
    #print(f"Updated Total payments: {updated_total_payments}")
    schedule = mortgage_dict[mortgage.mortgage_ID].extra_principal_payments()
    #print(mortgage_dict[mortgage.mortgage_ID].details())
    print(schedule.to_string(index=False))
    #print(schedule.loc[[122]])

    print("\n*******************************************************\n")
    #interest = (monthly+extra amount) * totalpayments - principal


def lump_payment():
    """
    Calculates new payment and total interest with an extra lump principal payments
    """
    menu_screen()
    cprint("Calculate Mortgage Overpayments:\n", "green")

    principal = validate_value('Enter the remaining principal left on your loan in Euro: \n')
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value("Enter the remaining length of your mortgage in years: \n")

    lump_payment = validate_value('How much of a lump payment do you want to make? \n')
    
    # Creates Mortgage Instance with Current Mortgage inputs
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage)
    mortgage_dict[mortgage.mortgage_ID] = mortgage
    
    # Prints Current Mortgage Details
    cprint("\nCurrent Mortgage: ----------------------------------------", "light_yellow")
    print(mortgage.details())
    print("Your current monthly payment is: €{:,.2f}".format(mortgage.calculate_monthly_payment()))
    print("The current cost of the remainder of this mortgage is: €{:,.2f}".format(mortgage.calculate_lifetime_interest()))
    
    # Creates a new Mortgage Class Instance with the updated information and 
    # Prints Updated Mortgaged details after Lump Payment applied
    cprint("\nUpdated Mortgage: ----------------------------------------", "light_yellow")
    new_mortgage = Mortgage((principal-lump_payment), apr, remaining_length_of_mortgage)
    mortgage_dict[new_mortgage.mortgage_ID] = new_mortgage
    #new_mortgage.update_mortgage_data()
    print(new_mortgage.details())
    print("Your new monthly payment is: €{:,.2f}".format(new_mortgage.calculate_monthly_payment()))
    print("The updated cost of the remainder of this mortgage is: €{:,.2f}".format(new_mortgage.calculate_lifetime_interest()))
    print(f"Extra principal: €{lump_payment}")

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
            selection = int(input("Enter 1 for monthly overpayments,  2 for a lump overpayment \nor enter '0' to exit this menu: \n"))
            if selection == 0:
                menu_screen()
            elif selection == 1:
                extra_monthly_principal()
                is_valid = True
            elif selection == 2:
                lump_payment()
                is_valid = True
            else:
               cprint("That is not a valid option. Please choose one from the list above.", "red")
        except ValueError:
            cprint("Please enter a valid mortgage number", "red")


def amortization():
    """
    Allows user to view an amoritization for individual Mortgage details one at a time
    """
    menu_screen()
    if len(mortgage_dict) == 0:
        cprint("This feature requires you to add at least one mortgage. Add a mortgage to proceed.", "red")
    else:
        cprint("You have entered the following mortgages:\n", "green")
        for x in mortgage_dict:
            print(f"Mortgage: {x}")
        
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
                            clear()
                            cprint(f"AMORTIZATION SCHEDULE FOR:", "yellow")
                            schedule = mortgage_dict[x].calculate_amortization_schedule()
                            print(mortgage_dict[x].details())
                            print(schedule.to_string(index=False))
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
        cprint("This feature requires you to add at least one mortgage. Add a mortgage to proceed.", "red")
    else:
        cprint("The Mortgage Averages collected:\n", "green")
        table = [
            ['Principal', 'APR', 'Loan Length', 'Monthly Payment', 'Total Interest'],
            ['350000', '4.3', '19', '2249.22', '162822.16'],
            ['350000', '4.3', '19', '2249.22', '162822.16'],
            ['350000', '4.3', '19', '2249.22', '162822.16']
            ]

        print(tabulate(table))
        print("\n*******************************************************")


def run_mortgage_tool():
    """
    Allows the user to select from various menu options for the Mortgage Comparison Tool
    """
    is_valid = False
    while is_valid != True:
        try:
            selection = int(input("Enter a selection from the Main Menu: \n"))
            if selection == 1:
                create_mortgage()
            elif selection == 2:
                view_mortgage()
                print("\n")
            elif selection == 3:
                compare_mortgages()
            elif selection == 4:
                overpayments()
            elif selection == 5:
                amortization()
            elif selection == 6:
                print("Option 6: Exit the program.")
                is_valid = True
            elif selection ==7:
                print("Mortgage Metrics Table")
            elif selection == 0:
                menu_screen()
            else:
                print("That is a not a valid option. Please type in a number between 1 - 7 or 0.")
        except ValueError:
            print("That is not a valid input. Please type in a number between 1 - 7 or 0.")    


if __name__ == '__main__':
    welcome_screen()
    menu_screen()
    run_mortgage_tool()
    




