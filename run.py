import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
"""
code to check if configuraion is set corectly

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)
"""

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")
        
        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
        #print(sales_data)
        #print(f"The data provided is {data_str} ")
    
    return sales_data

def validate_data(values):
    """
    Validate sales data entered
    Inside the try, converts all string values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
            f'Exactly six values required, you provided {len(values)}'
            )
        

    except ValueError as e:
        print(f'Invalid data: {e}, please try again\n')
        return False

    return True

def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list
    """
    print('Updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated!\n')

def update_surplus_worksheet(data):
    """
    update surplus worksheet, add new row with the list
    """
    print('Updating surplus worksheet...\n')
    sales_worksheet = SHEET.worksheet('surplus')
    sales_worksheet.append_row(data)
    print('Surplus worksheet updated!\n')

def update_worksheet(data, worksheet):
    """
    REFACTORING - Refactoring is the restructuring of code  
    to improve its operation, without altering its  functionality

    update relevant worksheet, add new row with the list
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated!\n')


def calculate_surplus_data(sales_row):
    """
    stock - sales
    positive = waste
    negative = surplus
    """
    print('Calculating surplus...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

    #print(surplus_data)
    #print(f'stock: {stock_row}')
    #print(f'sales: {sales_row}')

def get_last_5_entries_sales():
    """
    Collects collumns of data from las 5 sales from sales worksheet and return as list of list
    """
    sales = SHEET.worksheet("sales")
    #column = sales.col_values(3)

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        #print(column)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate average stock for each sandwich adding 10%
    """
    print('Calculating stock data... \n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data
    #print(data) 


def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    #update_sales_worksheet(sales_data)
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    #update_surplus_worksheet(new_surplus_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')
    print(stock_data)

print('Welcome to sandwich data automation')
main()
# run in command line - python3 run.py
