from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# Google sheets integration imports
import gspread
import datetime
from gspread_formatting import *

# Connecting to googlesheets
gc = gspread.service_account(filename='..\calorieassistant-SACred.json')
sh = gc.open('CaloriesSheet') # Open spreadsheet
worksheet_dave = sh.get_worksheet(0) # First Worksheet Dave Calories 
worksheet_meg = sh.get_worksheet(1) # Second Worksheet Meg Calories


def query_calories(worksheet):
    '''
    #TODO: change add calories logic
    This function will return the the calories stored on sheets if the row exists.
    It will return the number if there is already a record with today's date there.
    If the row doesn't exist then create it with 0 calories.
    '''

    # First need to get data as it could have changed inside of the loop
    data = worksheet.get('A1:B')    # Get all data ignoring the headers

    most_recent_date_str = data[-1][0] # Get lasts item from list / most recent record. First index which is date 
    most_recent_date_dt = datetime.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()

    today = datetime.date.today()
    today_formatted = today.strftime("%Y-%m-%d")

    if most_recent_date_dt < today:
        # then today's date isnt in the spreadsheet
        # Add new row
        print('Adding new row to table')
        total_calories = 0
        values = [today_formatted, total_calories]
        # Adding to the first row that's not full
        worksheet.insert_row(values, index=len(data)+1, value_input_option='USER_ENTERED')

    elif most_recent_date_dt == today:
        # Get current calories from the existing record
        print('Reading from existing row')
        current_calories = int(data[-1][1].replace(',','')) # Last row, calories item, parsed from string to int
 
        total_calories=current_calories

    # Inserting any dates turns type into string, thing this will fix this and allow us set all of that column to string
    fmt = cellFormat(
        horizontalAlignment='RIGHT',
        numberFormat=NumberFormat('DATE','yyyy-mm-dd')
        )
    format_cell_range(worksheet, 'A2:A', fmt)    

    return(total_calories)    ## Return this so Barry can say how many calories I have left

def add_calories(new_calories, worksheet):
    '''
    This function is used to add rows to the attached google sheets workbook.
    It will update the spreadsheet if there is already a record with todays date there.
    Otherwise it will create a new record with today's date
    '''

    # First need to get data as it could have changed inside of the loop
    data = worksheet.get('A1:B')    # Get all data ignoring the headers

    most_recent_date_str = data[-1][0] # Get lasts item from list / most recent record. First index which is date 
    most_recent_date_dt = datetime.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()

    today = datetime.date.today()
    today_formatted = today.strftime("%Y-%m-%d")

    if most_recent_date_dt < today:
        # then today's date isnt in the spreadsheet
        # Add new row
        print('Adding new row to table')
        total_calories = new_calories
        values = [today_formatted, total_calories]
        # Adding to the first row that's not full
        worksheet.insert_row(values, index=len(data)+1, value_input_option='USER_ENTERED')

    elif most_recent_date_dt == today:
        # Get current calories from the existing record
        # Add my new calories to the total
        print('Updating existing row')
        current_calories = int(data[-1][1].replace(',','')) # Last row, calories item, parsed from string to int
        total_calories = current_calories + new_calories
        values = [today_formatted, total_calories]
        # Delete existing and add new row over
        worksheet.delete_rows(len(data))
        worksheet.insert_row(values, index=len(data), value_input_option='RAW')

    # Inserting any dates turns type into string, thing this will fix this and allow us set all of that column to string
    fmt = cellFormat(
        horizontalAlignment='RIGHT',
        numberFormat=NumberFormat('DATE','yyyy-mm-dd')
        )
    format_cell_range(worksheet, 'A2:A', fmt)    

    return(total_calories)    ## Return this so Barry can say how many calories I have left




@app.route('/')
def index():

    dave_calories = query_calories(worksheet_dave)
    meg_calories = query_calories(worksheet_meg)

    return render_template('index.html', dave_calories=dave_calories, meg_calories=meg_calories)

@app.route('/action')
def action():
    print('starting action')
    command = request.args.get('command', default ='add', type = str)
    amount = request.args.get('amount', default =0, type = int)

    if command == 'add':
        # todo call add calories
        res = add_calories(amount, worksheet_dave)
    elif command == 'minus':
        # minus calories
        print()
    
    dave_calories = query_calories(worksheet_dave)
    meg_calories = query_calories(worksheet_meg)

    #return render_template('index.html', dave_calories=dave_calories, meg_calories=meg_calories)
    return jsonify(result=dave_calories)

@app.route('/action2')
def action2():
    print('starting action 2')
    command = request.args.get('command', default ='add', type = str)
    amount = request.args.get('amount', default =0, type = int)

    if command == 'add':
        # todo call add calories
        res = add_calories(amount, worksheet_dave)
    elif command == 'minus':
        # minus calories
        print()
    
    dave_calories = query_calories(worksheet_dave)

    return jsonify(result=dave_calories)

@app.route('/who')
def who():
    return 'Made By Dave'