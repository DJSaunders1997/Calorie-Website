from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import datetime
today = datetime.datetime.today().strftime("%Y-%m-%d")

import DBConModule

@app.route('/')
@app.route('/<date>')
#default date will be today
def index(date=today):

    #convert date from string to datetime    
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    global global_date
    global_date = date # update global date so add route can access

    #print(date.strftime("%Y-%m-%d"))

    dave_calories = DBConModule.get_daily_total('Dave', date)
    meg_calories = DBConModule.get_daily_total('Meg', date)

    #pass through date object to html so we can increment the day there.
    #will convert to string before showing it.
    return render_template('index.html', date=date, dave_calories=dave_calories, meg_calories=meg_calories, datetime=datetime)

# Changed from Messy Action to just an add rout
# Default will be me and 0 calories
@app.route('/add/<person>/<amount>')
# @app.route('/add/<person>/<date>/<amount>')
def add(person='Dave', amount='0'):
    
    #convert date from string to datetime
    #date = datetime.datetime.strptime(date, "%Y-%m-%d")

    print(person, global_date.strftime("%Y-%m-%d %H:%M:%S"), amount)

    # Cast amount to int before adding
    DBConModule.add_calories(person, global_date, int(amount))
    res = DBConModule.get_daily_total(person, global_date)

    return jsonify(result=res)


@app.route('/who')
def who():
    return 'Made By Dave'


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port="5000")
    app.run()