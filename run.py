"""
Libraries and Imports
"""
import gspread
from google.oauth2.service_account import Credentials
import math
import sys
from colorama import init
from termcolor import cprint
import pyfiglet
from tabulate import tabulate
import os

init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("mortgage_calculator")


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
    cprint(logo_text, "light_cyan")
    print("Welcome to my Mortgage Comparison Tool\n")
    proceed = input("Press the enter key to proceed \n").lower()


def print_main_menu():
    """ Prints the Main Menu """
    MENU_OPTIONS = """
You have the following options:
--------------------------------------------------------------
1. Add a mortgage               5. View Amortization Schedules
2. View a mortgage              6. Mortgage Metrics
3. Display Mortgage Comparison  7. Exit Program
4. Calculate Overpayments
--------------------------------------------------------------

"""
    print(MENU_OPTIONS)


def menu_screen():
    """
    Display Menu options
    """
    clear_screen()
    cprint("** Mortgage Calculator Tool **", "light_cyan")
    print_main_menu()


def print_data_analysis_intro():
    data_analysis_text = """
Mortgage Comparison Tool Data analysis:

The following are averages taken from the mortgages inputed into this
mortgage tool. See where your mortgage needs compare against the averages
of the mortgages entered into this program.

**********************************************************

    """
    print(data_analysis_text)


class Mortgage:
    """
    Base Class for Mortgages - creates a mortgage class instance
    """

    mortgage_ID = 0
    start_year = 0  # start of mortgage
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
        """Displays the Mortgage Profile Details"""
        return f"\nMORTGAGE: {self.mortgage_name} \nPrincipal: €{self.principal} \nLength of Mortgage: {self.length_of_mortgage} years \nAnnual Percentage Rate: {self.apr}%"

    def calculate_monthly_payment(self):
        """Calculates the monthly payments"""
        monthly_payment = round(
            ((self.apr / 100 / 12) * self.principal)
            / (
                1
                - (
                    math.pow(
                        (1 + (self.apr / 100 / 12)), (-self.length_of_mortgage * 12)
                    )
                )
            ),
            2,
        )
        return monthly_payment

    def calculate_lifetime_interest(self):
        """Calculates the liftetime interest or cost of a loan"""
        total_interest = round(
            (self.length_of_mortgage * 12 * self.calculate_monthly_payment())
            - self.principal,
            2,
        )
        return total_interest

    def get_table_values(self):
        """Creates mortgage values for comparison table"""
        row = [
            self.mortgage_name,
            "€{:,.2f}".format(self.principal),
            self.apr,
            self.length_of_mortgage,
            "€{:,.2f}".format(self.calculate_monthly_payment()),
            "€{:,.2f}".format(self.calculate_lifetime_interest()),
        ]
        return row

    def extra_principal_payments(self):
        """
        Calculates an updated Amorization Schedule when extra principal are
        applied to a loan.
        """
        updated_schedule = [
            [
                "Mon.",
                "Payment",
                "Principal",
                "Xtra Princ",
                "Interest",
                "Balance"
                ]
        ]
        balance = self.principal
        rate = self.apr / 100 / 12
        total_payments = self.length_of_mortgage * 12
        monthly_payment = self.calculate_monthly_payment()
        extra_monthly_principal = self.extra_monthly_principal
        for Month in range(1, total_payments):
            interest_payment = balance * rate
            principal_payment = monthly_payment - interest_payment
            new_principal_payment = principal_payment + extra_monthly_principal
            balance -= new_principal_payment
            total_payments -= 1
            if balance > 0:
                updated_schedule.append(
                    [
                        Month,
                        "€{:,.2f}".format(monthly_payment),
                        "€{:,.2f}".format(principal_payment),
                        "€{:,.2f}".format(extra_monthly_principal),
                        "€{:,.2f}".format(interest_payment),
                        "€{:,.2f}".format(balance),
                    ]
                )
        return updated_schedule

    def calculate_amortization_schedule(self):
        """Calculates the amortization schedule for a loan"""
        schedule = [
            [
                "Month",
                "Pmts Left",
                "Payment",
                "Principal",
                "Interest",
                "Balance"
                ]
        ]
        balance = self.principal
        rate = self.apr / 100 / 12
        total_payments = self.length_of_mortgage * 12
        monthly_payment = self.calculate_monthly_payment()
        for Month in range(1, total_payments):
            interest_payment = balance * rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            total_payments -= 1
            schedule.append(
                [
                    Month,
                    total_payments,
                    " €{:,.2f}".format(monthly_payment),
                    " €{:,.2f}".format(principal_payment),
                    " €{:,.2f}".format(interest_payment),
                    " €{:,.2f}".format(balance),
                ]
            )
        return schedule

    def create_mortgage_data(self):
        """
        Creates a string of mortgage data for a Mortgage Profile to
        export to Google Sheets
        """
        monthly_payment = self.calculate_monthly_payment()
        interest = self.calculate_lifetime_interest()
        data = [
            self.principal,
            self.apr,
            self.length_of_mortgage,
            monthly_payment,
            interest,
        ]
        return data

    def update_mortgage_data(self):
        """Exports the data for a mortgage to Google Sheets"""
        data = self.create_mortgage_data()
        mortgage_worksheet = SHEET.worksheet("mortgage_data")
        mortgage_worksheet.append_row(data)

    def calculate_mortgage_metrics(self):
        """
        Calculate the average principal, APR, loan length, monthly payment, and
        lifetime interest amount from aggregate data collected from all
        mortgage data stored in Google Sheets
        """
        mortgage_data = []
        mortgage_worksheet = SHEET.worksheet("mortgage_data").get_all_values()
        for column in mortgage_worksheet:
            avg = sum([int(y) for y in column]) / (len(mortgage_worksheet))
            avg = math.ceil(avg)
            mortgage_data.append(avg)

        return mortgage_data


def validate_value(prompt_text):
    """
    Prompts user for input and validates that input is an integer greater
    than 0.
    """
    while True:
        try:
            value = int(input(prompt_text))
            if value > 0:
                break
            else:
                cprint("Invalid. "
                       "Enter a whole number greater than 0", "light_red")
        except ValueError:
            cprint("That is not a valid input. "
                   "Enter a whole number.", "light_red")
    return value


def validate_apr():
    """
    Prompts user for input and validates that the input is a float
    with a value between 0 and 100.
    """
    while True:
        try:
            apr = float(input("Enter the Annual Percentage "
                              "rate or APR (e.g. 4.3): \n"))
            if apr > 0 and apr < 100:
                break
            else:
                cprint(
                    "APR must be greater than 0 but less than 100. "
                    "Enter a valid APR.",
                    "light_red",
                )
        except ValueError:
            cprint("That is not a number. Enter a valid number.", "light_red")
    return apr


def validate_name(prompt_text):
    """
    Prompts user for input and validates that the input is a string of
    10 characters or less
    """
    while True:
        try:
            name = str(input(prompt_text))
            if len(name) > 0 and len(name) < 11:
                break
            else:
                cprint(
                    "There is a maximum of 10 characters. Enter a valid name.",
                    "light_red",
                )
        except ValueError:
            cprint("That is not a valid entry. "
                   "Enter a valid name.", "light_red")
    return name


def display_mortgage_details(mortgage):
    """Displays the details of a Mortgage Profile"""
    print(mortgage.details())
    print("Monthly Payment: €{:,."
          "2f}".format(mortgage.calculate_monthly_payment()))
    print("Cost of this loan: €{:,."
          "2f}".format(mortgage.calculate_lifetime_interest()))
    print("\n")


def display_selected_mortgage(selection):
    """Creates and displays a list of user-saved Mortgage profiles"""
    for x in mortgage_dict:
        if selection == x:
            display_mortgage_details(mortgage_dict[x])
            break
        else:
            cprint("Please enter a mortgage in the list above.", "light_red")


def adds_mortgage_instance_to_dict(mortgage):
    """Adds the Mortgage Class Instance to the global mortgage dictionary"""
    while True:
        try:
            answer = str(
                input("\nWould you like to save this mortgage? Type Y or N \n")
            ).lower()
            if answer == "y":
                mortgage_dict[mortgage.mortgage_ID] = mortgage
                cprint(
                    "\nThanks. Your mortgage has been saved to your mortgages "
                    "in this session.",
                    "light_yellow",
                )
                break
            elif answer == "n":
                cprint(
                    "\nThis mortgage was NOT SAVED to your mortgages "
                    "in this session.",
                    "light_red",
                )
                break
            else:
                cprint("Please enter Y or N to proceed", "light_red")
        except ValueError:
            cprint(
                "Please enter the number of the mortgage you want to select.",
                "light_red",
            )


def calculate_average(data):
    """
    - Creates a new list from the items in the last column of
      Google Sheets data
    - Removes the Header from the list
    - Calculates an average of values in the list
    """
    column = []
    for x in data:
        last_item = x.pop()
        column.append(last_item)

    column.pop(0)

    total = 0
    for x in column:
        total += float(x)

    average = total / len(column)
    return average


def create_mortgage():
    """
    Creates each Class Instance of a Mortgage
    - Requests user input for the Name, Principal amount, APR amount, and
      Length of Mortgage
    - Creates the Mortgage class instance
    - Sends that data for storage in Google Sheets
    - Prints the Mortgage Profile
    - Requests user input to save Mortgage Profile for session
    """
    clear_screen()
    cprint("*** ADD A MORTGAGE *** \n", "light_green")
    cprint("Enter Your Mortgage details in below:\n", "light_green")

    # Request input from the user
    mortgage_name = validate_name(
        "Enter a name for this mortgage. You can use up to 10 characters. \n"
    )
    principal = validate_value("Enter the principal or loan amount "
                               "in Euro: \n")
    apr = validate_apr()
    length_of_mortgage = validate_value(
        "Enter the length of the mortgage in years (e.g. 30): \n"
    )

    # Creates a Mortgage Class Instance and adds it to the mortgage dictionary
    mortgage = Mortgage(principal, apr, length_of_mortgage, mortgage_name)

    # Creates a list of the mortgage data that appends to Google Sheets for
    # future analysis
    mortgage.update_mortgage_data()

    # Prints the Mortgage details just entered
    cprint("\nYou created a Mortgage with the following details:",
           "light_yellow")
    display_mortgage_details(mortgage)

    # Allows user to save mortgage for the session
    adds_mortgage_instance_to_dict(mortgage)

    print("\n*******************************************************\n")


def view_mortgage():
    """
    Allows user to choose an individual Mortgage Profile to view
    """
    clear_screen()
    cprint("*** VIEW A MORTGAGE *** \n", "light_green")

    # Prints a column of the available Mortgage Class Instances
    if len(mortgage_dict) == 0:
        cprint(
            "This feature requires you to add at least one mortgage.\n"
            "Add a mortgage to proceed.",
            "light_red",
        )
    else:
        cprint("You have entered the following mortgages:\n", "light_green")
        for x in mortgage_dict:
            print(f"Mortgage: # {x}, {mortgage_dict[x].mortgage_name}")

        # Prompts user to select a mortgage to view or user can select to
        # return to main menu
        print("\n")
        while True:
            try:
                selection = int(
                    input(
                        "Enter the number of the mortgage that you'd like to "
                        "view \nor enter '0' to return to the main menu: \n"
                    )
                )
                if selection == 0:
                    menu_screen()
                    break
                else:
                    display_selected_mortgage(selection)
                    cprint("(Enter 0 to view the Main menu)", "light_green")
            except ValueError:
                cprint(
                    "Please enter the number of the mortgage you want to "
                    "select.",
                    "light_red",
                )

    print("\n*******************************************************\n")


def compare_mortgages():
    """
    Displays a comparison table of all the Mortgage Profiles saved by the user
    """
    clear_screen()
    cprint("*** COMPARE MORTGAGES *** \n", "light_green")

    if len(mortgage_dict) < 2:
        cprint(
            "This feature requires you to add at least two mortgage.\n"
            "Add mortgages to proceed.",
            "light_red",
        )
    else:
        mortgage_table = [
            [
                "Mortgage",
                "Principal",
                "APR %",
                "Loan\nLength",
                "Monthly\nPayment",
                "Total\nInterest",
            ]
        ]

        cprint("\nMORTGAGE COMPARISON TABLE\n", "light_yellow")
        for x in mortgage_dict:
            mortgage_table.append(mortgage_dict[x].get_table_values())

        print(tabulate(mortgage_table, tablefmt="simple"))

    print("\n******************************************************* \n")


def extra_monthly_principal():
    """
    Calculates a revised Amortization Principal Payment when extra monthly
    payments are made
    - Requests input from the user to create Mortgage Profile
    - Requests input from the user for amount of extra monthly principal
      payments

    """
    clear_screen()
    cprint("Calculate Mortgage Monthly Overpayments on an existing "
           "mortgage:\n", "light_green")

    # Request user input for original loan
    mortgage_name = validate_name(
        "Enter a name for this mortgage. You can use up to 10 characters. \n"
    )
    principal = validate_value(
        "Enter the remaining principal left on your existing loan in Euro: \n"
    )
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value(
        "How many years are left on your mortgage?  (e.g. 30) \n"
    )

    # Request user input for extra monthly principal payment amount
    extra_principal = validate_value(
        "Enter the extra principal you would like to pay each month: \n"
    )

    # Creates a new Mortgage Profile with the extra monthly principal
    # payment applied
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage,
                        mortgage_name)
    mortgage.extra_monthly_principal = extra_principal

    # Displays the original Mortgage profile
    cprint("\nCurrent Mortgage: ", "light_yellow")
    display_mortgage_details(mortgage)

    # Prints the updated amortization schedule for the revised Mortgage profile
    print("\n**********************************************\n")
    cprint("UPDATED MORTGAGE AMORTIZATION SCHEDULE:", "light_yellow")

    print("Extra Monthly Principal Payment: €{:,."
          "2f}".format(extra_principal), "\n")
    schedule = mortgage.extra_principal_payments()
    print(tabulate(schedule, headers="firstrow", tablefmt="github"))

    print("\n*******************************************************\n")


def lump_payment():
    """
    Calculates new payment and total interest with an extra lump
    principal payments
    """
    clear_screen()
    cprint("Calculate Mortgage Lump Overpayments:\n", "light_green")

    # Requests User input to create Current Mortgage profile
    mortgage_name = validate_name(
        "Enter a name for this mortgage. You can use up to 10 characters. \n"
    )
    principal = validate_value(
        "Enter the remaining principal left on your loan in Euro: \n"
    )
    apr = validate_apr()
    remaining_length_of_mortgage = validate_value(
        "Enter the remaining length of your mortgage in years: \n"
    )

    lump_payment = validate_value("How much of a lump payment do you "
                                  "want to make? \n")

    # Creates Mortgage Instance with Current Mortgage inputs
    mortgage = Mortgage(principal, apr, remaining_length_of_mortgage,
                        mortgage_name)

    # Prints Current Mortgage Details
    cprint(
        "\nCurrent Mortgage: ----------------------------------------",
        "light_yellow"
    )
    display_mortgage_details(mortgage)

    # Creates an Updated Mortgage Class Instance and prints updated information
    cprint(
        "\nUPDATED Mortgage: ----------------------------------------",
        "light_yellow"
    )
    new_mortgage = Mortgage(
        (principal - lump_payment), apr, remaining_length_of_mortgage,
        mortgage_name
    )
    display_mortgage_details(new_mortgage)
    print(f"Principal Lump Overpayment: €{lump_payment}")

    print("\n*******************************************************\n")


def overpayments():
    """
    Gives User the selection of making monthly overpayments or
    lump sum overpayment
    """
    clear_screen()
    cprint("*** MORTGAGE OVERPAYMENTS *** \n", "light_green")

    while True:
        try:
            selection = int(
                input(
                    "Enter 1 for Extra Monthly Principal overpayments, "
                    "2 for a Lump Principal overpayment, \nor enter '0' "
                    "to exit this menu: \n"
                )
            )
            if selection == 0:
                break
            elif selection == 1:
                extra_monthly_principal()
            elif selection == 2:
                lump_payment()
            else:
                clear_screen()
                cprint(
                    "That is not a valid option. Please choose one from "
                    "the list above.",
                    "light_red",
                )
        except ValueError:
            clear_screen()
            cprint("Please enter a valid mortgage number", "light_red")

    menu_screen()


def amortization():
    """
    Allows user to view an amoritization for individual Mortgage profile
    """
    clear_screen()
    cprint("*** VIEW AN AMORTIZATION FOR A MORTGAGE *** \n", "light_green")

    if len(mortgage_dict) == 0:
        cprint(
            "This feature requires you to add at least one mortgage.\n"
            "Add a mortgage to proceed.",
            "light_red",
        )
    else:
        cprint("You have entered the following mortgages:\n", "light_green")
        for x in mortgage_dict:
            print(f"Mortgage: # {x}, {mortgage_dict[x].mortgage_name}")

        print("\n")
        while True:
            try:
                selection = int(
                    input(
                        "Enter the number of the mortgage that you'd like "
                        "to amortize \nor enter '0' to "
                        "return to the main menu: \n"
                    )
                )
                if selection == 0:
                    menu_screen()
                    break
                else:
                    for x in mortgage_dict:
                        if selection == x:
                            cprint(f"\n\nAMORTIZATION SCHEDULE FOR:",
                                   "light_yellow")
                            schedule = mortgage_dict[
                                x
                            ].calculate_amortization_schedule()
                            display_mortgage_details(mortgage_dict[x])
                            print(
                                tabulate(
                                    schedule,
                                    headers="firstrow",
                                    tablefmt="github"
                                )
                            )
                            print("\n")
                            is_valid = True
                        else:
                            continue
            except ValueError:
                print("Please enter a correct number")

    print("\n*******************************************************\n")


def print_mortgage_avg():
    """
    Prints averages of data stored in Google Sheets in a table
    """
    mortgage_data = []
    mortgage_worksheet = SHEET.worksheet("mortgage_data").get_all_values()
    for row in mortgage_worksheet:
        mortgage_data.append(row)

    # Gets the calculations for the averages of Lifetime Interest,
    # Monthly payments, Loan length, APR, and Principal amounts
    interest_average = calculate_average(mortgage_data)
    monthly_payment_average = calculate_average(mortgage_data)
    loan_length_average = calculate_average(mortgage_data)
    apr_average = calculate_average(mortgage_data)
    principal_average = calculate_average(mortgage_data)

    # Prints the averages
    print_data_analysis_intro()
    cprint("Average Principal: €{:,.2f}".format(principal_average),
           "light_yellow")
    cprint(f"Average APR: {round(apr_average, 1)}%", "light_yellow")
    cprint(
        f"Average Loan Length {math.floor(loan_length_average)} years",
        "light_yellow"
    )
    cprint(
        "Average Monthly Payment: €{:,.2f}".format(monthly_payment_average),
        "light_yellow",
    )
    cprint(
        "Average Lifetime Interest: €{:,.2f}".format(interest_average),
        "light_yellow"
    )

    print("\n*******************************************************")


def main_menu():
    """
    Main menu:
    - Allows the user to select from various Main Menu options for the
      Mortgage Comparison Tool
    """
    while True:
        try:
            selection = int(input("Enter a selection from the Main Menu: \n"))
            if selection == 1:
                create_mortgage()
                cprint("(Enter 0 to view the Main menu)", "light_green")
            elif selection == 2:
                view_mortgage()
                cprint("(Enter 0 to view the Main menu)", "light_green")
            elif selection == 3:
                compare_mortgages()
                cprint("(Enter 0 to view the Main menu)", "light_green")
            elif selection == 4:
                overpayments()
                cprint("(Enter 0 to view the Main menu)", "light_green")
            elif selection == 5:
                amortization()
                cprint("(Enter 0 to view the Main menu)", "light_green")
            elif selection == 6:
                clear_screen()
                cprint("Calculating Mortgage Analysis...", "light_green")
                print_mortgage_avg()
                cprint("(Enter 0 to view the Main menu)", "light_green")
            elif selection == 7:
                clear_screen()
                cprint(
                    "\n\nThanks for using the Mortgage Comparison Tool.\n",
                    "light_yellow",
                )
                break
            elif selection == 0:
                menu_screen()
            else:
                cprint(
                    "That is not a menu option. Type in a number between 1 - 7"
                    " or 0 for the main menu.",
                    "light_red",
                )
        except ValueError:
            cprint(
                "That is not a valid input. Please type in a number between "
                "1 - 7 or 0.",
                "light_red",
            )


def main():
    """Main function"""
    welcome_screen()
    menu_screen()
    main_menu()


if __name__ == "__main__":
    main()
